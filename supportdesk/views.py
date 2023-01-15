from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import ListView, View
from django.views.generic.edit import FormView
from django.contrib.auth.models import User

from django.urls import reverse_lazy

from .forms import RequestForm
from .models import RequestModel


class RegisterView(FormView):
    template_name = "supportdesk/request.html"
    login_url = reverse_lazy('login')
    form_class = RequestForm
    success_url = reverse_lazy("request")

    def form_valid(self, form):
        # creating request for user
        form.save()
        return redirect(self.success_url)
    
    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)
        user_request_count = RequestModel.objects.filter(user=self.request.user.id).count()
        context['form'] = form
        context['user_request_count'] =user_request_count
        return self.render_to_response(context)

class MyRequestsView(ListView):
    template_name = "supportdesk/my_requests.html"
    model = RequestModel
    context_object_name = "myrequests"
    paginate_by = 4

    def get_queryset(self):
        # lisitng user's request 
        return RequestModel.objects.filter(
            user=self.request.user
        ).order_by('-created_at')


class StaffRequestsView(ListView):
    template_name = "supportdesk/staff_requests.html"
    model = RequestModel
    context_object_name = "staff_requests"
    paginate_by = 3
    
    def get(self, request):
        staff_requests = RequestModel.objects.filter(
            assignee=self.request.user,
        ).order_by('-created_at')

        # sending completed and in progress requests
        return render ( request, "supportdesk/staff_requests.html", context={
            "staff_requests":staff_requests.filter(status = "I"),
            "staff_completed":staff_requests.filter(status = "C"),
        } )

    def post(self, request ):

        request_id = request.POST.get('request_id')
        reassign = request.POST.get('reassign')
        
        # reassigning request to other staff
        if reassign:
            try:
                # getting request
                single_request =  RequestModel.objects.get(pk=reassign, assignee_id = request.user.id)
            except RequestModel.DoesNotExist:
                return render(request, "supportdesk/invalid.html")
            # getting the staff
            staff = User.objects.filter( is_staff = True).exclude(id=single_request.assignee.id).order_by('?').first()
            # changing the staff
            single_request.assignee = staff
            single_request.save()
            context_requests = RequestModel.objects.filter(
                    assignee=self.request.user
                                ).order_by('-created_at')   
            context = {
                "staff_requests":context_requests
            }

            return render(request, "supportdesk/staff_requests.html", context)

        # changing to completed status
        if request_id:
            try:
                # finding request
                single_request =  RequestModel.objects.get(pk=request_id, assignee_id = request.user.id)
            except RequestModel.DoesNotExist:
                return render(request, "supportdesk/unauthorized.html")
            context_requests = RequestModel.objects.filter(
                    assignee=self.request.user
                                ).order_by('-created_at')   
            context = {
                "staff_requests":context_requests
            }
            # changing state
            single_request.status = "C"
            single_request.save()
            return render(request, "supportdesk/staff_requests.html", context)
        else:
            return render(request, "supportdesk/invalid.html", context)


# Single request
class StaffSingleRequestView(View):

    def get(self, request, pk):
        try:
            single_request =  RequestModel.objects.get(pk=pk, assignee_id = request.user.id)
        except RequestModel.DoesNotExist:
            return render(request, "supportdesk/unauthorized.html")
        context = {
            "single_request":single_request
        }
        return render(request, "supportdesk/single_request.html", context)

    def post(self, request, pk):
        # changing single request status to completed
        try:
            single_request =  RequestModel.objects.get(pk=pk, assignee_id = request.user.id)
        except RequestModel.DoesNotExist:
            return render(request, "supportdesk/unauthorized.html")
        context = {
            "single_request":single_request
        }
        single_request.status = "C"
        single_request.save()
        return render(request, "supportdesk/single_request.html", context)

    