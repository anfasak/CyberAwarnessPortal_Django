from django.contrib import admin
from django.urls import path
from CyberAwarnessGameApp import views
from CyberAwarnessGameApp.views import *

urlpatterns = [

    # Admin Home
    path('', views.AdminHome.as_view(), name='AdminHome'),

    # Login
    path('LoginPage/', views.LoginPage.as_view(), name='LoginPage'),

    # Complaints
    path('ViewComplaint/', views.ViewComplaint.as_view(), name='ViewComplaint'),
    path('SendReply/<int:id>/', views.SendReply.as_view(), name='SendReply'),

    # Feedback
    path('ViewFeedback/', views.ViewFeedback.as_view(), name='ViewFeedback'),

    # Users
    path('ViewUser/', views.ViewUser.as_view(), name='ViewUser'),
    
    path('add_manage_learn/', views.ViewContent.as_view(), name='add_manage_learn'),
    
    path('addlink/', views.Addurls.as_view(), name='addlink'),

    path('DeleteLink/<int:id>', views.DeleteLink.as_view(), name='DeleteLink'),

    path('Add_learn_modules', views.AddLearning.as_view(), name='Add_learn_modules'),
    
    path('ManageLInk/', views.ManageLink.as_view(), name='ManageLink'),

    path('ViewQuiz/', views.quiz.as_view(), name='ViewQuiz'),

    path('AddQuiz/',views.ManageQuiz.as_view(), name='AddQuiz'),

    path('DeleteQuiz/<int:id>', views.DeleteQuiz.as_view(), name='DeleteLink'),

    path('QuizResult/',views.ViewResult.as_view(), name='QuizResult'),
    path('GenerateCertificate/<int:id>/', views.GenerateCertificate.as_view(), name='GenerateCertificate'),
    path('GetCertificate/<int:id>/', views.GetCertificate.as_view(), name='GetCertificate'),

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),



    


################################################  API  ###########################################

    path('userregister', UserReg_api.as_view()),
    path('LoginAPI', LoginPageAPI.as_view()),
    path('ForgotPasswordAPI', ForgetPassword.as_view()),
    path('feedback/<int:id>', ViewFeedbackAPI.as_view()),
    path('complaint/<int:id>',ViewComplaintAPI.as_view()),
    path('viewcontents', ViewContentAPI.as_view()),
    path('viewquiz', ViewQuizAPI.as_view()),
    path('submit/<int:id>', SubmitResultAPI.as_view()),
    path('ViewResult/<int:id>', ViewResultAPI.as_view()),
    path('viewprofile/<int:id>', ViewProfileAPI.as_view()),
    path('editprofile/<int:id>',EditProfileAPI.as_view()),
    path('otpverification', SendOTP.as_view()),
    path('chat-history<int:lid>',ViewChatbotHistoryAPI.as_view()),
    path('GetCertificateAPI/<int:id>/', GetCertificateAPI.as_view())
    




]
