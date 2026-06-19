from django.db import models


class LoginTable(models.Model):
    username = models.CharField(max_length=300, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    user_type = models.CharField(max_length=30, blank=True, null=True)



class UserTable(models.Model):
    login = models.ForeignKey(LoginTable, on_delete=models.CASCADE)
    Name= models.CharField(max_length=300, blank=True, null=True)
    Emailid = models.EmailField(max_length=500, blank=True, null=True)
    PhoneNumber= models.CharField(max_length=150, blank=True, null=True)
    profileImage=models.FileField(upload_to='profile/', null=True, blank=True)


    

class ComplaintTable(models.Model):
    User = models.ForeignKey(UserTable, on_delete=models.CASCADE,null=True, blank=True)
    Complaint = models.TextField(blank=True, null=True)
    Reply = models.TextField(blank=True, null=True)
    Date = models.DateField(auto_now_add=True)



class FeedbackTable(models.Model):
    User = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    Feedback = models.TextField(blank=True, null=True)
    Rating = models.FloatField(blank=True, null=True)
    Date = models.DateField(auto_now_add=True)
 

class LearningTable(models.Model):
    image=models.FileField(upload_to='images/', null=True, blank=True)
    Content=models.CharField(max_length=200, blank=True, null=True)
    Description=models.CharField(max_length=1000, blank=True, null=True)
    ThreatType=models.CharField(max_length=200, blank=True, null=True)
    Link=models.CharField(max_length=200, blank=True, null=True)

class LinkTable(models.Model):
    Modules = models.ForeignKey(LearningTable, on_delete=models.CASCADE)
    Link = models.CharField(max_length=20, blank=True, null=True)  
   

class QuizTable(models.Model):
    question=models.CharField(max_length=100, blank=True, null=True)
    option1=models.CharField(max_length=100, blank=True, null=True)
    option2=models.CharField(max_length=100, blank=True, null=True)
    option3=models.CharField(max_length=100, blank=True, null=True)
    answer=models.CharField(max_length=100, blank=True, null=True)
    

class ResultTable(models.Model):
    quiz = models.ForeignKey(QuizTable, on_delete=models.CASCADE)
    userid = models.ForeignKey(UserTable, on_delete=models.CASCADE, null=True, blank=True)
    selected_index = models.IntegerField()
    is_correct = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

class CertificateTable(models.Model):
    Userid = models.ForeignKey(UserTable, on_delete=models.CASCADE, null=True, blank=True)
    resultid = models.ForeignKey(ResultTable, on_delete=models.CASCADE, null=True, blank=True)
    certificate = models.FileField(upload_to='certificate/', null=True, blank=True)



class OTPModel(models.Model):
    email = models.CharField(null=True, max_length=100)
    otp = models.IntegerField(null=True)
    otp_verified = models.BooleanField(blank=True, default=False)


class ChatHistory(models.Model):
    user = models.ForeignKey(UserTable, on_delete=models.CASCADE, null=True, blank=True)
    user_input = models.TextField(null=True, blank=True)
    ai_response = models.TextField(null=True, blank=True)