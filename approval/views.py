from django.http import JsonResponse
from django.shortcuts import render
from base.models import Shift, Sector, Emplo_Schedu, Employee


def approval_director(request):
    shifts = Shift.objects.all()
    sectors = Sector.objects.all()

    data = {
        'shifts': shifts,
        'sectors': sectors
    }
    return render(request, 'approval_director.html', data)


def director_list(request):
    shifts_request = int(request.GET['shift'])
    sector_request = int(request.GET['sector'])
    date_request = request.GET['date']

    leaders = []

    if shifts_request == 0:
        shifts = [shift.to_json() for shift in Shift.objects.all()]
        emplo_schedus_full = Emplo_Schedu.objects.prefetch_related('employee', 'scheduling').filter(
            scheduling__date=date_request)
        emplo_schedus = [emplo_schedus.to_json() for emplo_schedus in emplo_schedus_full.order_by('employee__name')]

        for emp_sch in emplo_schedus_full.order_by('employee__leader_name'):
            leader = Employee.objects.get(name=emp_sch.employee.leader_name).to_json()
            if not leader in leaders:
                leaders.append(leader)

    else:
        shifts = Shift.objects.get(id=shifts_request).to_json()
        emplo_schedus_full = Emplo_Schedu.objects.prefetch_related('employee', 'scheduling').filter(
            scheduling__date=date_request, scheduling__shift_id=shifts_request)

        emplo_schedus = [emplo_schedus.to_json() for emplo_schedus in emplo_schedus_full.order_by('employee__name')]
        for emp_sch in emplo_schedus_full.order_by('employee__leader_name'):
            leader = Employee.objects.get(name=emp_sch.employee.leader_name).to_json()
            if not leader in leaders:
                leaders.append(leader)

    if sector_request == 0:
        sectors = [sector.to_json() for sector in Sector.objects.all().order_by('name')]
    else:
        sectors = Sector.objects.get(id=sector_request).to_json()

    response = {
        'shifts': shifts,
        'sectors': sectors,
        'emplo_schedus':emplo_schedus,
        'leaders':leaders
    }

    return JsonResponse(response)
