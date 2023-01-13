from django import forms
from .models import RequestModel
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field

class RequestForm(forms.ModelForm):
    summary = forms.CharField(label="Summary", max_length=100, widget=forms.TextInput(attrs={'placeholder': "Unable to login to application"}))
    description = forms.Field(label="Description",widget=forms.Textarea)
    priority_flag = forms.CharField(label="Flag" ,widget=forms.CheckboxInput(attrs={"class": "slider form-control"}))
    
    class Meta:
        model = RequestModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Field('notify_faculty_field', css_class="form-check-input", wrapper_class="form-check form-switch"),
        )