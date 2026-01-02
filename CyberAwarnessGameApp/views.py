from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from .serializers import *

from .forms import *
from CyberAwarnessGameApp.models import *


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
            d=ContentForm(request.POST,request.FILES)
            if d.is_valid():
                d.save()
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

