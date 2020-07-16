from django.contrib import admin
from .models import Sector, SubSector, Employee, UserProfileInfo, Shift


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


admin.site.register(Employee, Employees)

admin.site.register(SubSector)
admin.site.register(Sector)
admin.site.register(UserProfileInfo)
admin.site.register(Shift)
