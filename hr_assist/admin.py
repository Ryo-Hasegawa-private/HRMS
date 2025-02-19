from django.contrib import admin

from .models import Employee
from .models import Allowance
    
admin.site.register(Employee)
admin.site.register(Allowance)