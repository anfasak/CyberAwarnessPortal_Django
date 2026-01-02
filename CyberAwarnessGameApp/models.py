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
    Content=models.CharField(max_length=50, blank=True, null=True)
    Description=models.CharField(max_length=500, blank=True, null=True)
    ThreatType=models.CharField(max_length=50, blank=True, null=True)
    Link=models.CharField(max_length=200, blank=True, null=True)

class LinkTable(models.Model):
    Modules = models.ForeignKey(LearningTable, on_delete=models.CASCADE)
    Link = models.CharField(max_length=20, blank=True, null=True)  
   

class QuizTable(models.Model):
    question=models.CharField(max_length=20, blank=True, null=True)
    option1=models.CharField(max_length=20, blank=True, null=True)
    option2=models.CharField(max_length=20, blank=True, null=True)
    option3=models.CharField(max_length=20, blank=True, null=True)
    answer=models.CharField(max_length=20, blank=True, null=True)
    