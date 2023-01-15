from django.urls import path
from .views import RegisterView, PlaceholderHome, MyRequestsView

urlpatterns = [
    path(
        "placeholder/", PlaceholderHome.as_view(), name="supportdesk_placeholder"
    ),
    path("request/", RegisterView.as_view(), name = "request"),
    path("my_requests/", MyRequestsView.as_view(), name="myrequests")
]
