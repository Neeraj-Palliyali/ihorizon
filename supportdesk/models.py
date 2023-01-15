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
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name="user")
    assignee = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING, related_name="assignee")
    status = models.CharField(choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0], max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.summary + "|" + str(self.user.first_name) + "|" + str(self.created_at.date())
    
    @property
    def get_lifetime(self) -> str:
        time_gap = datetime.now(timezone.utc) - self.created_at
        if time_gap.days<=0:
            if (time_gap.seconds/(60**2))<=1:
                if (time_gap.seconds/(60))<=1:
                    return str(int(time_gap.seconds)) + " Seconds "
                else:
                    return str(int(time_gap.seconds/60)) + " Minutes "
            else:
                return str(int(time_gap.seconds/(60**2))) + " Minutes "
        else:
            return str(time_gap.days) + " days "
    
    @property
    def get_asignee(self)->str:
        # To get and assign the request to a staff
        if self.assignee:
            return self.assignee.username 

        else:
            assignee =  User.objects.filter(is_staff = True).order_by('?').first()
            self.assignee = assignee
            self.save()
            return self.assignee.username


