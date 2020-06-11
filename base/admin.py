from django.contrib import admin
from .models import Sector, SubSector, Employee, UserProfileInfo,Shift

# Register your models here.
admin.site.register(Employee)
admin.site.register(SubSector)
admin.site.register(Sector)
admin.site.register(UserProfileInfo)
admin.site.register(Shift)
