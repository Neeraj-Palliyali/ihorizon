from django.urls import path
from .views import RegisterView, MyRequestsView, StaffRequestsView, StaffSingleRequestView


urlpatterns = [
    path("request/", RegisterView.as_view(), name = "request"),
    path("my_requests/", MyRequestsView.as_view(), name="myrequests"),
    path("staff_requests/", StaffRequestsView.as_view(), name="staff_requests"),
    path("staff_requests/<pk>/", StaffSingleRequestView.as_view(), name="single_request"),
]
