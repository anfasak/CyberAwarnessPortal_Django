from django.forms import ModelForm

from .models import *


class LinkForm(ModelForm):
    class Meta:
        model=LinkTable
        fields='__all__'
class ContentForm(ModelForm):
    class Meta:
        model=LearningTable
        fields='__all__'       


class ReplyForm(ModelForm):
    class Meta:
        model = ComplaintTable
        fields = ['Reply']

class QuizForm(ModelForm):
    class Meta:
        model=QuizTable
        fields='__all__'        