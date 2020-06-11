from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from base.models import Shift, Employee, Emplo_Schedu, Scheduling, Sector


def report_shift(request):
    shifts = Shift.objects.all()
    data = {'shifts': shifts}
    return render(request, 'report_shift.html', data)


def shift_preview(request):
    date = request.GET['date']
    shift_params = int(request.GET['shift'])

    if shift_params != 0:
        shifts_res = Shift.objects.filter(id=int(shift_params))
        emplo_schedus = Emplo_Schedu.objects.prefetch_related('employee', 'scheduling').filter(
            scheduling__date=date,scheduling__shift_id=shift_params)
        shifts_res = [shift.to_json() for shift in shifts_res]
    else:
        shifts_res_date = Shift.objects.all()
        shifts_res = [shift.to_json() for shift in shifts_res_date]
        emplo_schedus = Emplo_Schedu.objects.prefetch_related('employee', 'scheduling').filter(
            scheduling__date=date)

    leaders = []
    for emplo_schedu in emplo_schedus:
        leader = Employee.objects.get(name=emplo_schedu.employee.leader_name).to_json()
        if not leader in leaders:
            leaders.append(leader)

    sectors = [sector.to_json() for sector in Sector.objects.all()]

    emplo_schedus_data = [emplo_schedu.to_json() for emplo_schedu in emplo_schedus]
    date_split = date.split('-')
    formatted_date = date_split[2] + "/" + date_split[1] + "/" +date_split[0]
    response = {
        'emplo_schedus_data': emplo_schedus_data,
        'shifts_res': shifts_res,
        'leaders':leaders,
        'sectors':sectors,
        'date':formatted_date,
    }
    return JsonResponse(response)
