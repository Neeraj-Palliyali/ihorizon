from django.urls import path
from . import views

urlpatterns = [
    path(
        "placeholder/", views.PlaceholderHome.as_view(), name="supportdesk_placeholder"
    ),
    path("request/", views.RegisterView.as_view(), name = "request")
]
