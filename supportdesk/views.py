from . import forms
from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.shortcuts import redirect


class PlaceholderHome(TemplateView):
    template_name = "supportdesk/placeholder.html"


class RegisterView(FormView):
    template_name = "supportdesk/request.html"
    form_class = forms.RequestForm
    success_url = reverse_lazy("request")

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)