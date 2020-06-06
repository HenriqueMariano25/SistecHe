from django.http import HttpResponse
from django.shortcuts import render
from base.models import Shift, Employee, Emplo_Schedu, Scheduling, Sector


# Create your views here.
def report_shift(request):
    global shifts_res
    shifts = Shift.objects.all()
    data = {'shifts': shifts}
    if request.method == "POST":
        date = request.POST['date']
        shift_params = request.POST['shift']
        if shift_params != '0':
            shifts_res = Shift.objects.get(id=int(shift_params))
            emplo_schedus = Emplo_Schedu.objects.prefetch_related('employee', 'scheduling').filter(
                scheduling__date=date,
                scheduling__sector_id=int(
                    shift_params))
        else:
            shifts_res = shifts
            emplo_schedus = Emplo_Schedu.objects.prefetch_related('employee', 'scheduling').filter(
                scheduling__date=date)

        leaders = []
        for emplo_schedu in emplo_schedus:
            leader = Employee.objects.get(name=emplo_schedu.employee.leader_name)
            if not leader in leaders:
                leaders.append(leader)

        sectors = Sector.objects.all()

        data = {'shifts': shifts, 'shifts_res': shifts_res, 'emplo_schedus': emplo_schedus, 'leaders':leaders, 'sectors':sectors}

    return render(request, 'report_shift.html', data)


def shift_preview(request):
    if request.method == "GET":
        date = request.GET['date']
        shift_params = request.GET['shift']
        shift = Shift.objects.all()
        shifts_res = shift
        employees = Emplo_Schedu.objects.prefetch_related('employee', 'scheduling').filter(scheduling__date=date)
        if shift_params != "0":
            employees = Emplo_Schedu.objects.prefetch_related('employee', 'scheduling').filter(scheduling__date=date,
                                                                                               scheduling__sector_id=int(
                                                                                                   shift_params))
            shifts_res = Shift.objects.get(id=int(shift_params))

        data = {
            'shifts': shift,
            'shifts_res': shifts_res,
        }
        pass
