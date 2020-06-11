from django import template
register = template.Library()

from base.models import Shift

@register.filter()
def emplo_in_leader(leader, employees):
    shifts = []
    emplo_schedus = employees.filter(employee__leader_name=leader.name)
    for emplo_schedu in emplo_schedus:
        shift = Shift.objects.get(id=emplo_schedu.scheduling.shift.id)
        if not shift in shifts:
            shifts.append(shift)

    return shifts
