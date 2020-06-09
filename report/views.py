from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from base.models import Shift, Employee, Emplo_Schedu, Scheduling, Sector


# Create your views here.
def report_shift(request):
    global shifts_res
    shifts = Shift.objects.all()
    data = {'shifts': shifts}
    # if request.method == "POST":
    #     date = request.POST['date']
    #     shift_params = request.POST['shift']
    #     if shift_params != '0':
    #         shifts_res = Shift.objects.get(id=int(shift_params))
    #         emplo_schedus = Emplo_Schedu.objects.prefetch_related('employee', 'scheduling').filter(
    #             scheduling__date=date,
    #             scheduling__sector_id=int(
    #                 shift_params))
    #     else:
    #         shifts_res = shifts
    #         emplo_schedus = Emplo_Schedu.objects.prefetch_related('employee', 'scheduling').filter(
    #             scheduling__date=date)
    #
    #     leaders = []
    #     for emplo_schedu in emplo_schedus:
    #         # scheduling = Scheduling.objects.get(id=emplo_schedu.)
    #         leader = Employee.objects.get(name=emplo_schedu.employee.leader_name)
    #         if not leader in leaders:
    #             leaders.append(leader)
    #
    #
    #
    #     sectors = Sector.objects.all()
    #
    #     data = {'shifts': shifts, 'shifts_res': shifts_res, 'emplo_schedus': emplo_schedus, 'leaders':leaders, 'sectors':sectors}

    return render(request, 'report_shift.html', data)


def shift_preview(request):
    # print(request.GET)
    date = request.GET['date']
    shift_params = request.GET['shift']

    if shift_params != '0':
        shifts_res = Shift.objects.get(id=int(shift_params)).to_json()
        emplo_schedus = Emplo_Schedu.objects.prefetch_related('employee', 'scheduling').filter(
            scheduling__date=date,
            scheduling__sector_id=int(
                shift_params))
    else:
        shifts_res_date = Shift.objects.all()
        # print(shifts_res_date)
        shifts_res = [shift.to_json() for shift in shifts_res_date]
        # for shift in shifts_res_date:
        #     print(shift)
        emplo_schedus = Emplo_Schedu.objects.prefetch_related('employee', 'scheduling').filter(
            scheduling__date=date)
    #
    leaders = []
    for emplo_schedu in emplo_schedus:
        # scheduling = Scheduling.objects.get(id=emplo_schedu.)
        leader = Employee.objects.get(name=emplo_schedu.employee.leader_name).to_json()
        print(leader)
        if not leader in leaders:
            leaders.append(leader)

    sectors = [sector.to_json() for sector in Sector.objects.all()]

    emplo_schedus_data = [emplo_schedu.to_json() for emplo_schedu in emplo_schedus]
    print(emplo_schedus_data)
    print(shifts_res)
    print(leaders)
    print(sectors)
    response = {
        'emplo_schedus_data': emplo_schedus_data,
        'shifts_res': shifts_res,
        'leaders':leaders,
        'sectors':sectors,
    }
    return JsonResponse(response)
