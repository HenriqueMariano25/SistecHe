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


def search_employee_scheduling(request):
    search = request.GET['search']
    if 'search' in request.GET:
        employees = Employee.objects.filter(name__icontains=search, sector=request.user.userprofileinfo.sector)
        print(employees)
        leaders_res = []
        leaders_burst_res = []
        employees_res = []
        employees_burst_res = []
        for employee in employees:
            employees_json_obj = dict(name=employee.name, id=employee.id, registration=employee.registration,
                            occupation=employee.occupation, extra_hour=employee.extra_hour,
                            leader_name=employee.leader_name)

            leader = Employee.objects.get(name=employee.leader_name)
            leader_json_obj = dict(name=leader.name)

            print(employee.extra_hour)

            if employee.extra_hour + 7.30 > 24.0:
                employees_burst_res.append(employees_json_obj)
                if not leader_json_obj in leaders_burst_res:
                    leaders_burst_res.append(leader_json_obj)
            else:
                employees_res.append(employees_json_obj)
                if not leader_json_obj in leaders_res:
                    leaders_res.append(leader_json_obj)

        data = {'leaders': leaders_res,
                'employees': employees_res,
                'employees_burst': employees_burst_res,
                'leaders_burst': leaders_burst_res,}

    return HttpResponse(json.dumps(data), content_type='application/json')