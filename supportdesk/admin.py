from django.contrib import admin

from .models import RequestModel

class RequestDetailsAdmin(admin.ModelAdmin):
    list_display = ('summary',)

admin.site.register(RequestModel, RequestDetailsAdmin)
