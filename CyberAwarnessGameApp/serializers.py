from CyberAwarnessGameApp.models import *
from rest_framework.serializers import ModelSerializer

class LoginTableSerializer(ModelSerializer):
    class Meta:
        model = LoginTable
        fields = ['username', 'password', 'user_type']


class RegsiterTableSerializer(ModelSerializer):
    class Meta:
        model = UserTable
        fields = ['Name', 'Emailid', 'PhoneNumber', 'login']
        extra_kwargs = {
            'login': {'read_only': True}
        }


class ComplaintTableSerializer(ModelSerializer):
    class Meta:
        model=ComplaintTable
        fields='__all__'
        
class  FeedbackTableSerializer(ModelSerializer):
    class Meta:
        model=FeedbackTable
        fields=['Feedback','Rating']

class LearningTableSerializer(ModelSerializer):
    class Meta:
        model=LearningTable
        fields=['Content','Description','ThreatType','Link','image']                  
class LinkTableSerializer(ModelSerializer):
    class Meta:
        model=LinkTable
        fields=['Modules','Link'] 

class QuizTableSerializers(ModelSerializer):
    class Meta:
        model=QuizTable
        fields='__all__'

class ResultTableSerializers(ModelSerializer):
    class Meta:
        model=ResultTable
        fields='__all__'                   