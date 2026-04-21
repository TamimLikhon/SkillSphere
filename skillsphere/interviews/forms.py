from django import forms
from .models import Interview, Interviewer, Shortlist


class InterviewerForm(forms.ModelForm):
    class Meta:
        model = Interviewer
        fields = '__all__'


class ShortlistForm(forms.ModelForm):
    class Meta:
        model = Shortlist
        fields = '__all__'


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = '__all__'