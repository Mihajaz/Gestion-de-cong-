from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Employee , LeaveRequest
# Register your models here.

admin.site.register(Employee)
admin.site.register(LeaveRequest)
admin.site.register(Permission)