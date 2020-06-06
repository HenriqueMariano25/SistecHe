from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from base.models import Employee, Shift, Scheduling, Emplo_Schedu
import json
from django.core.serializers.json import DjangoJSONEncoder


def scheduling_employees(request):
    print(Scheduling.objects.all())
    leaders = Employee.objects.filter(leader=True, sector=request.user.userprofileinfo.sector)
    shifts = Shift.objects.all()

    data = {"leaders": leaders, "shifts": shifts}

    return render(request, 'scheduling_employees.html', data)


def selected_leader(request):
    leader = Employee.objects.get(id=request.GET['lider_id'])
    employees = Employee.objects.filter(leader_name=leader.name)
    employees_res = []
    for employee in employees:
        json_obj = dict(name=employee.name, id=employee.id, registration=employee.registration,
                        occupation=employee.occupation, extra_hour=employee.extra_hour)
        employees_res.append(json_obj)

    data = {
        "employees": employees_res,
        "leader": dict(name=leader.name, occupation=leader.occupation)
    }
    return HttpResponse(json.dumps(data), content_type='application/json')


def finalize_employee_scheduling(request):

    print(request.POST)
    scheduling_date = request.POST['scheduling_date']
    reason = request.POST['reason']
    registrations = request.POST.getlist('registrations')
    shift = request.POST['shift']

    scheduling = Scheduling(date=scheduling_date, reason=reason, shift_id=int(shift), user=request.user,
                            sector=request.user.userprofileinfo.sector)

    if scheduling.save:
        scheduling.save()

    for registration in registrations:
        print(registration)
        employee = Employee.objects.get(registration=registration)
        print(employee)
        emplo_sched = Emplo_Schedu(scheduling=scheduling, employee=employee)
        if emplo_sched.save:
            emplo_sched.save()
    messages.success(request, "Agendamento realizado com sucesso")
    return redirect('scheduling_employees')
