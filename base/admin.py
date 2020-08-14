from django.contrib import admin
from .models import Sector, SubSector, Employee, UserProfileInfo, Shift, Scheduling, Emplo_Schedu


# Register your models here.
class Employees(admin.ModelAdmin):
    list_display = (
        'name', 'registration', 'admission_date', 'demission_date', 'leader', 'leader_name', 'manager',
        'occupation',
        'extra_hour', 'sector', 'sub_sector')
    list_display_links = ('name', 'registration')
    search_fields = ('name', 'registration')
    list_per_page = 30
    ordering = ('name',)


class Schedulings(admin.ModelAdmin):
    list_display = (
        'date', 'reason', 'shift', 'user', 'sector')
    list_display_links = ('date', 'reason')
    search_fields = ('date', 'reason', 'sector')
    list_per_page = 100
    ordering = ('date',)

class Emplo_Schedus(admin.ModelAdmin):
    list_display = (
        'employee', 'scheduling', 'plus_he', 'authorized')
    list_display_links = ('employee', 'scheduling')
    search_fields = ('employee', 'scheduling')
    list_per_page = 100
    ordering = ('scheduling',)


admin.site.register(Employee, Employees)
admin.site.register(Scheduling, Schedulings)
admin.site.register(Emplo_Schedu, Emplo_Schedus)

admin.site.register(SubSector)
admin.site.register(Sector)
admin.site.register(UserProfileInfo)
admin.site.register(Shift)
