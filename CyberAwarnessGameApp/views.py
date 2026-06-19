from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from CyberAwarnessGame import settings

from .serializers import *

from .forms import *
from CyberAwarnessGameApp.models import *

from django.core.validators import validate_email
import random
from django.core.mail import send_mail
import os

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import io


class LoginPage(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            obj = LoginTable.objects.get(username=username, password=password)
            request.session['user_id'] = obj.id

            if obj.user_type == 'admin':
                return HttpResponse(
                    '''<script>alert("Login successful");window.location='/AdminHome/'</script>'''
                )
            else:
                return HttpResponse(
                    '''<script>alert("Login successful");window.location='/'</script>'''
                )

        except LoginTable.DoesNotExist:
            return HttpResponse(
                '''<script>alert("Invalid credentials");window.location='/LoginPage/'</script>'''
            )


class ViewComplaint(View):
    def get(self, request):
        complaints = ComplaintTable.objects.all()
        return render(request, 'view_complaint_and_send_replay.html', {'f': complaints})


class ViewFeedback(View):
    def get(self, request):
        feedbacks = FeedbackTable.objects.all()
        return render(request, 'view_feedback.html', {'a': feedbacks})



class ViewUser(View):
    def get(self, request):
        users = UserTable.objects.all()
        return render(request, 'view_user.html', {'c': users})


class AdminHome(View):
    def get(self, request):
        return render(request, 'admin_home.html')


class SendReply(View):
    def post(self, request, id):
        obj = ComplaintTable.objects.get(id=id)
        reply = ReplyForm(request.POST, instance=obj)
        if reply.is_valid():
            reply.save()
            return redirect('/ViewComplaint/')

class ViewContent(View):
    def get(self, request):
        Link=LearningTable.objects.all()
        return render(request,'add_manage_learn.html',{'w':Link})

class Addurls(View):
     def get(self, request):
        return render(request, 'addlink.html')
     
     def post(self, request):
         r=LinkForm(request.POST)
         if r.is_valid():
             r.save()
             return redirect('/addlink/')

class DeleteLink(View):
    def get(self,request,id):
        try:
            d=LearningTable.objects.get(id=id) 
            d.delete()
            return HttpResponse('''<script>alert(" link delete successfully");window.location='/add_manage_learn'</script>''')
        except LearningTable.DoesNotExist:
                return HttpResponse('''<script>alert(" link not found");window.location='/add_manage_learn'</script>''')


class AddLearning(View):
    def get(self, request):
        return render(request,'Add_learn_modules.html')
    
    def post(self, request):
            print('-------------', request.POST)
            print('-------------', request.FILES)
            # d=ContentForm(request.POST,request.FILES)
            # if d.is_valid():
            #     d.save()
            #     return redirect('/add_manage_learn')
            Content = request.POST['Content']
            ThreatType = request.POST['ThreatType']
            Description = request.POST['Description']
            Link = request.POST['Link']
            image = request.FILES['image']
            obj = LearningTable()
            obj.Content=Content
            obj.ThreatType=ThreatType
            obj.Description=Description
            obj.Link=Link
            obj.image=image
            obj.save()


            return redirect('/add_manage_learn')

class ManageLink(View):
     def get(self, request):
         c=LearningTable.objects.all()
         return render(request, 'Add_and_manage_Link.html',{'ww':c})

    
class ManageQuiz(View):
    def get(self, request):
        return render(request,'Quiz.html') 
    def post(self, request):
         r=QuizForm(request.POST)
         if r.is_valid():
             # Enforce 100 question limit
             count = QuizTable.objects.count()
             if count >= 100:
                 oldest = QuizTable.objects.order_by('id').first()
                 if oldest:
                     oldest.delete()
             
             r.save()
             return redirect('/ViewQuiz/')
         
class DeleteQuiz(View):
    def get(self,request,id):
        try:
            d=QuizTable.objects.get(id=id) 
            d.delete()
            return HttpResponse('''<script>alert(" link delete successfully");window.location='/ViewQuiz'</script>''')
        except QuizTable.DoesNotExist:
                return HttpResponse('''<script>alert(" link not found");window.location='/ViewQuiz'</script>''')      

class quiz(View):
   def get(self,request):
         c=QuizTable.objects.all()
         return render(request, 'ViewQuiz.html',{'questions':c})
   
# from django.views import View
# from django.shortcuts import render
# from django.db.models import Count, Q
# from .models import ResultTable, QuizTable, UserTable

# class ViewResult(View):
#     def get(self, request):
#         total_questions = QuizTable.objects.count()

#         users = UserTable.objects.all()
#         user_results = []

#         for user in users:
#             results = ResultTable.objects.filter(userid=user)

#             correct_count = results.filter(is_correct=True).count()

#             user_results.append({
#                 'user': user,
#                 'correct': correct_count,
#                 'total': total_questions,
#                 'results': results
#             })

#         return render(request, 'ViewQuizResult.html', {
#             'user_results': user_results
#         })

             

from django.views import View
from django.shortcuts import render
from django.db.models import Count
from .models import ResultTable, QuizTable

class ViewResult(View):
    def get(self, request):
        total_questions = QuizTable.objects.count()

        # 🔹 Get only users who attended quiz
        user_results = (
            ResultTable.objects
            .values('userid')
            .annotate(correct=Count('id', filter=models.Q(is_correct=True)))
        )

        summary = []
        for ur in user_results:
            userid = ur['userid']
            correct = ur['correct']
            
            user_obj = ResultTable.objects.filter(userid=userid).first().userid
            cert_exists = CertificateTable.objects.filter(Userid=user_obj).exists()

            summary.append({
                'user': user_obj,
                'correct': correct,
                'total': total_questions,
                'cert_exists': cert_exists
            })

        return render(request, 'ViewQuizResult.html', {
            'summary': summary
        })

from django.shortcuts import render, redirect
from .models import *

# ================= ADMIN DASHBOARD =================
def admin_dashboard(request):

    user_count = UserTable.objects.count()
    feedback_count = FeedbackTable.objects.count()
    complaint_count = ComplaintTable.objects.count()
    quiz_result_count = ResultTable.objects.count()

    context = {
        'user_count': user_count,
        'feedback_count': feedback_count,
        'complaint_count': complaint_count,
        'quiz_result_count': quiz_result_count,
    }

    return render(request, 'admin_home.html', context)   


    
#///////////////////////////////////////////////////////////////////////////////////
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserReg_api(APIView):
    def post(self, request):
        print("###################", request.data)

        user_serial = RegsiterTableSerializer(data=request.data)
        login_serial = LoginTableSerializer(data=request.data)

        user_valid = user_serial.is_valid()
        login_valid = login_serial.is_valid()

        print(user_valid)
        print(login_valid)

        if user_valid and login_valid:
            login_profile = login_serial.save(user_type='USER')
            user_serial.save(login=login_profile)

            return Response(user_serial.data, status=status.HTTP_201_CREATED)

        return Response(
            {
                "login_error": login_serial.errors,
                "user_error": user_serial.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    
class LoginPageAPI(APIView):
    def post(self,request):

        response_dict={}
        username=request.data.get("username")
        password=request.data.get("password")

        if not username or not password:
            response_dict["message"]="failed"
            return Response(response_dict, status=status.HTTP_400_BAD_REQUEST)
        t_user=LoginTable.objects.filter(username=username, password=password).first()

        if not t_user:
            response_dict["message"]= "failed"
            return Response(response_dict,status=status.HTTP_401_UNAUTHORIZED)
        else:
            response_dict["message"]="success"
            response_dict["username"]=t_user.id 
            response_dict["user_type"]=t_user.user_type

            return Response(response_dict, status=status.HTTP_200_OK)
        
class ViewFeedbackAPI(APIView):
    def post(self,request,id):
        print(request.data)
        user = UserTable.objects.get(login__id=id)
        serializer=FeedbackTableSerializer (data=request.data) 
        if serializer.is_valid():
             serializer.save(User=user)
             return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewComplaintAPI(APIView):
    def post(self,request,id):
        print(request.data)
        c=UserTable.objects.get(login_id=id)
        print(c)
        serializer=ComplaintTableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(User=c)
            return Response(serializer.data,status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, id):
        c=UserTable.objects.get(login__id=id)
        Complaints=ComplaintTable.objects.filter(User=c)
        serializer=ComplaintTableSerializer(Complaints,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ViewLinkAPI(APIView):
    def post(self,request,id):
        d=LinkTable.objects.get(LOGIN_id=id)
        serializer=LinkTableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(User=d)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class ViewContentAPI(APIView):
#     def post(self,request,id):
#         a=LearningTable.objects.get(Login_id=id)
#         serializer=LearningTableSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(User=a)
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ViewContentAPI(APIView):
    def get(self, request):
        data = LearningTable.objects.all()
        serializer = LearningTableSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

import random
    
class ViewQuizAPI(APIView):
    def get(self, request):
        quiz = list(QuizTable.objects.all())
        random.shuffle(quiz)  # 🔥 shuffle questions

        data = []

        for q in quiz:
            options = [
                {"text": q.option1, "index": 0},
                {"text": q.option2, "index": 1},
                {"text": q.option3, "index": 2},
                {"text": q.answer, "index": 3},
            ]

            random.shuffle(options)  # 🔥 shuffle options

            data.append({
                "quiz_id": q.id,
                "question": q.question,
                "options": options,
            })

        return Response(data, status=status.HTTP_200_OK)

class SubmitResultAPI(APIView):
    def post(self, request, id):
        user = UserTable.objects.get(login__id=id)

        quiz_id = request.data.get("quiz_id")
        selected_index = int(request.data.get("selected_index"))

        quiz = QuizTable.objects.get(id=quiz_id)

        # ✅ FIX: option 4 (index 3) is the correct answer
        is_correct = selected_index == 3

        ResultTable.objects.create(
            quiz=quiz,
            userid=user,
            selected_index=selected_index,
            is_correct=is_correct
        )

        return Response({
            "message": "Result saved",
            "selected_index": selected_index,
            "correct_option": quiz.answer,
            "is_correct": is_correct
        }, status=status.HTTP_200_OK)
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ResultTable, QuizTable, UserTable

class ViewResultAPI(APIView):
    def get(self, request, id):
        """
        id = login id of user
        """

        # 🔹 Get user
        user = UserTable.objects.get(login__id=id)

        # 🔹 Total questions in quiz table
        total_questions = QuizTable.objects.count()

        # 🔹 Results of this user
        user_results = ResultTable.objects.filter(userid=user)

        # 🔹 Correct answers count
        correct_answers = user_results.filter(is_correct=True).count()

        # 🔹 Prepare detailed result list
        result_list = []
        for r in user_results:
            result_list.append({
                "quiz_id": r.quiz.id,
                "question": r.quiz.question,
                "selected_index": r.selected_index,
                "is_correct": r.is_correct,
                "created_at": r.created_at,
            })

        return Response({
            "total_questions": total_questions,
            "attempted": user_results.count(),
            "correct_answers": correct_answers,
            "results": result_list,
        }, status=status.HTTP_200_OK)

class ViewProfileAPI(APIView):
      def get(self, request,id):
        data = UserTable.objects.filter(login__id=id)
        serializer = UserSerializers(data, many=True)
        print('------------>', serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    
class EditProfileAPI(APIView):
    def post(self, request, id):
        print('--------------', request.data)
        user = UserTable.objects.get(login__id=id)

        serializer = UserSerializers(
            user,
            data=request.data,
            partial=True   # ✅ IMPORTANT
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendOTP(APIView):
    def get(self, request):
        email = request.data.get('email')
        print('-----------', email)
        try:
            validate_email(email)

        except:
            return Response(
                {
                    'message': "Invalid Email",
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        existing_email = LoginTable.objects.filter(username=email).first()

        if existing_email:
            return Response(
                {
                    "message": "Email already exist"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        otp = random.randint(100000, 999999)
        print("otp", otp)
        send_mail(
            subject= " Your OTP for registering to cyber awareness ",
            message= f"Your OTP to register mil for the app is : {otp}",
            from_email= settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )
        print("--------------------------")

        OTPModel.objects.update_or_create(
            email = email,
            otp = otp,
            otp_verified = False
        )

        return Response({"message":"OTP sent successfully"}, status=status.HTTP_200_OK)
    
    def post(self, request):

        email = request.data.get('email')
        otp = request.data.get('otp')

        try:
            record = OTPModel.objects.get(email=email, otp=otp)
        except ValidationError:
            return Response({'message': "Invalid OTP"}, status=status.HTTP_401_UNAUTHORIZED)
        
        record.otp_verified = True

        record.save()

        return Response(data=record.otp_verified, status=status.HTTP_200_OK)
    

class ViewChatbotHistoryAPI(APIView):
    """
    View all chatbot conversations of a user
    """

    def get(self, request, lid):
        # Step 1: Validate user
        try:
            user = UserTable.objects.get(login__id=lid)
        except UserTable.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Step 2: Fetch chat history
        chats = ChatHistory.objects.filter(
            user=user
        ).order_by("-created_at")

        # Step 3: Serialize manually (simple & fast)
        data = []
        for chat in chats:
            data.append({
                "id": chat.id,
                "user_input": chat.user_input,
                "ai_response": chat.ai_response,
                "created_at": chat.created_at
            })

        return Response(
            {
                "user": user.Name,
                "total_chats": chats.count(),
                "chat_history": data
            },
            status=status.HTTP_200_OK
        )


class GenerateCertificate(View):
    def get(self, request, id):
        user = get_object_or_404(UserTable, id=id)
        
        # Calculate score
        results = ResultTable.objects.filter(userid=user)
        correct_count = results.filter(is_correct=True).count()
        total_questions = QuizTable.objects.count()

        # Ensure the greatest number is after the /
        display_score = min(correct_count, total_questions)
        display_total = max(correct_count, total_questions)
        
        # Create PDF in memory (Landscape)
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=landscape(letter))
        width, height = landscape(letter)
        
        # --- BACKGROUND & BORDERS ---
        # Outer Border (Navy)
        p.setStrokeColor(colors.navy)
        p.setLineWidth(5)
        p.rect(20, 20, width - 40, height - 40)
        
        # Inner Border (Gold)
        p.setStrokeColor(colors.goldenrod)
        p.setLineWidth(2)
        p.rect(35, 35, width - 70, height - 70)
        
        # Decorative Corners (Gold)
        p.setLineWidth(3)
        # Top-Left
        p.line(35, height - 100, 35, height - 35)
        p.line(35, height - 35, 100, height - 35)
        # Top-Right
        p.line(width - 100, height - 35, width - 35, height - 35)
        p.line(width - 35, height - 35, width - 35, height - 100)
        # Bottom-Left
        p.line(35, 100, 35, 35)
        p.line(35, 35, 100, 35)
        # Bottom-Right
        p.line(width - 100, 35, width - 35, 35)
        p.line(width - 35, 35, width - 35, 100)
        
        # --- TITLE SECTION ---
        p.setFillColor(colors.navy)
        p.setFont("Helvetica-Bold", 42)
        p.drawCentredString(width / 2, height - 130, "CERTIFICATE")
        
        p.setFont("Helvetica", 18)
        p.drawCentredString(width / 2, height - 160, "OF PARTICIPATION")
        
        # --- MAIN TEXT ---
        p.setStrokeColor(colors.black)
        p.setLineWidth(0.5)
        p.line(width/4, height - 180, 3*width/4, height - 180)
        
        p.setFillColor(colors.black)
        p.setFont("Helvetica", 20)
        p.drawCentredString(width / 2, height - 240, "This is to certify that")
        
        # Name
        p.setFillColor(colors.darkblue)
        p.setFont("Times-BoldItalic", 45)
        p.drawCentredString(width / 2, height - 310, user.Name or "Participant")
        
        # Divider Line under Name
        p.setStrokeColor(colors.goldenrod)
        p.setLineWidth(1)
        p.line(width/4, height - 325, 3*width/4, height - 325)
        
        # Achievement Message
        p.setFillColor(colors.black)
        p.setFont("Helvetica", 18)
        p.drawCentredString(width / 2, height - 370, "has successfully participated in the")
        p.setFont("Helvetica-Bold", 22)
        p.drawCentredString(width / 2, height - 400, "CYBER AWARENESS CHALLENGE")
        
        # Score Information
        p.setFont("Helvetica-Oblique", 16)
        p.drawCentredString(width / 2, height - 440, f"Achieving a score of {display_score} out of {display_total}")
        
        # --- FOOTER SECTION (Signatures & Date) ---
        # Date
        from datetime import date
        p.setFont("Helvetica", 14)
        p.drawString(100, 110, f"Date: {date.today().strftime('%B %d, %Y')}")
        p.line(100, 105, 250, 105) # Date underline
        
        # Signature Lines
        p.drawCentredString(width - 175, 110, "Authorized Signature")
        p.line(width - 250, 105, width - 100, 105)
        p.setFont("Helvetica-Oblique", 12)
        p.drawCentredString(width - 175, 90, "Cyber Awareness Program Director")
        
        # Seal Placment
        p.setStrokeColor(colors.goldenrod)
        p.setFillColor(colors.gold)
        p.circle(width/2, 100, 40, stroke=1, fill=1)
        p.setFillColor(colors.navy)
        p.setFont("Helvetica-Bold", 10)
        p.drawCentredString(width/2, 105, "OFFICIAL")
        p.drawCentredString(width/2, 95, "SEAL")
        
        # --- FINALIZATION ---
        p.showPage()
        p.save()
        
        # Save to Model
        pdf_data = buffer.getvalue()
        file_name = f"certificate_{user.id}_{date.today().strftime('%Y%m%d')}.pdf"
        
        # Link to the first result found for this user if exists (optional refinement)
        first_result = results.first()
        
        cert_obj = CertificateTable.objects.create(
            Userid=user,
            resultid=first_result
        )
        cert_obj.certificate.save(file_name, ContentFile(pdf_data))
        cert_obj.save()
        
        buffer.close()
        
        # Redirect back with success message
        return HttpResponse(f'''<script>alert("Landscape Certificate of Participation generated for {user.Name}");window.location='/QuizResult/'</script>''')

# class GenerateCertificate(View):
#     def get(self, request, id):
#         user = get_object_or_404(UserTable, id=id)
        
#         # Calculate score
#         results = ResultTable.objects.filter(userid=user)
#         correct_count = results.filter(is_correct=True).count()
#         total_questions = QuizTable.objects.count()

#         display_score = min(correct_count, total_questions)
#         display_total = max(correct_count, total_questions)
        
#         buffer = io.BytesIO()
#         p = canvas.Canvas(buffer, pagesize=landscape(letter))
#         width, height = landscape(letter)

#         # ---- CERTIFICATE BACKGROUND IMAGE ----
#         import os
#         from django.conf import settings
        
#         image_path = os.path.join(settings.BASE_DIR.parent, "static/certificate/certificate_template.jpg")
#         # Draw certificate template image
#         p.drawImage(image_path, 0, 0, width=width, height=height)

#         # ---- USER NAME ----
#         p.setFillColor(colors.black)
#         p.setFont("Helvetica-Bold", 36)
#         p.drawCentredString(width/2, height/2 + 30, user.Name or "Participant")

#         # ---- DATE ----
#         from datetime import date
#         today = date.today().strftime("%B %d, %Y")

#         p.setFont("Helvetica", 16)
#         p.drawCentredString(width/2 - 200, height/2 - 120, today)

#         # ---- CERTIFICATE NUMBER ----
#         cert_no = f"CG-{user.id}-{date.today().strftime('%Y%m%d')}"

#         p.setFont("Helvetica", 16)
#         p.drawCentredString(width/2 + 200, height/2 - 120, cert_no)

#         # ---- FINALIZE PDF ----
#         p.showPage()
#         p.save()
        
#         pdf_data = buffer.getvalue()
#         file_name = f"certificate_{user.id}_{date.today().strftime('%Y%m%d')}.pdf"
        
#         first_result = results.first()
        
#         cert_obj = CertificateTable.objects.create(
#             Userid=user,
#             resultid=first_result
#         )
#         cert_obj.certificate.save(file_name, ContentFile(pdf_data))
#         cert_obj.save()
        
#         buffer.close()
        
#         return HttpResponse(f'''<script>alert("Certificate generated for {user.Name}");window.location='/QuizResult/'</script>''')

class GetCertificate(View):
    def get(self, request, id):
        user = get_object_or_404(UserTable, id=id)
        cert = CertificateTable.objects.filter(Userid=user).order_by('-id').first()
        
        if cert and cert.certificate:
            return redirect(cert.certificate.url)
        else:
            return HttpResponse('''<script>alert("No certificate found for this user");window.location='/QuizResult/'</script>''')


class GetCertificateAPI(APIView):
    def get(self, request,id):
        data = CertificateTable.objects.filter(Userid__login=id)
        serializer = CertificateSerializers(data, many=True)
        print('------------>', serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK) 

from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages


class ForgetPassword(APIView):
    def post(self, request):
        print('-----------------', request.data)
        email = request.data.get('email')

        if not email:
            return Response({'message': "Email is required"},status=status.HTTP_401_UNAUTHORIZED)

        # List of user tables to check
        user_tables = [UserTable]

        for table in user_tables:
            try:
                user = table.objects.get(Emailid=email)
                login_obj = get_object_or_404(LoginTable, id=user.login.id)

                # Send email (Consider replacing this with a password reset link)
                send_mail(
                    'Password Recovery',
                    f'Your Account Password is: {login_obj.password}',
                    'cyberguard252@gmail.com',
                    [email],
                )

                messages.success(request, f'Password sent to {email}.')
                return Response(status=status.HTTP_200_OK)

            except table.DoesNotExist:
                continue  # Check the next table

        return Response(status=status.HTTP_204_NO_CONTENT)
    

