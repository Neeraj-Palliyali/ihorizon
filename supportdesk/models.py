from django.db import models

# Create your models here.
class RequestModel(models.Model):
    summary = models.CharField(verbose_name="Summary", max_length=100, )
    description = models.TextField(verbose_name="Description")
    priority_flag = models.BooleanField()