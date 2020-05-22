from django.contrib import admin
from .models import Sector, SubSector, Employee

# Register your models here.
admin.site.register(Employee)
admin.site.register(SubSector)
admin.site.register(Sector)
