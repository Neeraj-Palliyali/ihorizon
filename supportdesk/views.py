from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.urls import reverse
from django.urls import reverse_lazy

from .forms import RequestForm
from .models import RequestModel

class PlaceholderHome(TemplateView):
    template_name = "supportdesk/placeholder.html"


class RegisterView(FormView):
    template_name = "supportdesk/request.html"
    login_url = reverse_lazy('login')
    form_class = RequestForm
    success_url = reverse_lazy("request")

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)

class MyRequestsView(ListView):
    template_name = "supportdesk/my_requests.html"
    model = RequestModel
    context_object_name = "myrequests"
    paginate_by = 4

    def get_queryset(self):
        return RequestModel.objects.filter(
            user=self.request.user
        ).order_by('-updated_at')