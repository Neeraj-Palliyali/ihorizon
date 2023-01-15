from django import forms
from .models import RequestModel
from django.contrib.auth.models import User

class RequestForm(forms.ModelForm):
    # Form for a reqyest
    summary = forms.CharField(label="Summary", 
                                max_length=100, 
                                widget=forms.TextInput(
                                    attrs={'placeholder': "Unable to login to application"}))
    description = forms.Field(label="Description", widget=forms.Textarea, required=True)
    priority_flag = forms.BooleanField(label="Priority", required=False)
    user = forms.CharField(required=False)
    class Meta:
        model = RequestModel
        exclude = ('status',)

    def clean_user(self):
        data = self.cleaned_data['user']
        data = User.objects.get(id = data)
        return data
    
    def clean_priority_flag(self):
        data = self.cleaned_data['priority_flag']
        return data
