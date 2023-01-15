from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timezone
# Create your models here.
class RequestModel(models.Model):

    STATUS_CHOICES = (
        ( 'I', 'In Progress'),
        ( 'C', 'Completed'),
    )
    summary = models.CharField(verbose_name="Summary", max_length=100, blank=False)
    description = models.TextField(verbose_name="Description", blank=False)
    priority_flag = models.BooleanField(default=False)
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0], max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.summary + "|" + str(self.user.first_name) + "|" + str(self.created_at.date())
    
    @property
    def get_lifetime(self) -> datetime:
        return (datetime.now(timezone.utc) - self.created_at).days