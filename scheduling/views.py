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
    leaders = Employee.objects.filter(leader=True, sector=request.user.userprofileinfo.sector).order_by('name')
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
    print(scheduling_date)
    reason = request.POST['reason']
    registrations = request.POST.getlist('registrations[]')
    shift = request.POST['shift']

    scheduled_employees = []

    unscheduled_employees = []

    for registration in registrations:
        emplo_schedu = Emplo_Schedu.objects.filter(scheduling__date=scheduling_date,
                                                   employee__registration=registration).first()
        if not emplo_schedu is None:
            scheduled_employees.append(emplo_schedu.to_json())
            print("tem")
            print(emplo_schedu)
            continue
        else:
            print("nao tem")
            print(emplo_schedu)
            unscheduled_employees.append(registration)

    print(scheduled_employees)
    print(unscheduled_employees)

    if scheduled_employees:
        response = {
            'status' : 'success',
            'scheduled_employees' : scheduled_employees,
        }
    else:
        if unscheduled_employees:
            scheduling = Scheduling(date=scheduling_date, reason=reason, shift_id=int(shift), user=request.user,
                                    sector=request.user.userprofileinfo.sector)
            if scheduling.save:
                scheduling.save()

            for registration in unscheduled_employees:
                employee = Employee.objects.get(registration=registration)
                emplo_sched = Emplo_Schedu(scheduling=scheduling, employee=employee)
                if emplo_sched.save:
                    emplo_sched.save()

        response = {
            'status':'success',
            # 'scheduled_employees': scheduled_employees
        }
    return JsonResponse(response)

    # messages.error(request, "Teste")
    #
    # scheduling = Scheduling(date=scheduling_date, reason=reason, shift_id=int(shift), user=request.user,
    #                         sector=request.user.userprofileinfo.sector)
    #
    # if scheduling.save:
    #     scheduling.save()
    #
    # for registration in registrations:
    #
    #     employee = Employee.objects.get(registration=registration)
    #     emplo_sched = Emplo_Schedu(scheduling=scheduling, employee=employee)
    #     if emplo_sched.save:
    #         emplo_sched.save()
    # messages.success(request, "Agendamento realizado com sucesso")
    # return redirect('scheduling_employees')


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
                'leaders_burst': leaders_burst_res, }

    return HttpResponse(json.dumps(data), content_type='application/json')


def edit_scheduling_employees(request):
    return render(request, 'edit_scheduling_employees.html')


def edit_scheduling_employees_list(request):
    date = request.POST['date']
    emplo_schedus = Emplo_Schedu.objects.prefetch_related('employee', 'scheduling').filter(
        scheduling__date=date, employee__sector_id=request.user.userprofileinfo.sector_id, authorized=True)
    emplo_schedus_json = [emplo_schedu.to_json() for emplo_schedu in emplo_schedus]
    response = {
        'emplo_schedus': emplo_schedus_json,
    }
    return JsonResponse(response)


def delete_emplo_scheduling(request):
    registration = request.POST['registration']
    date = request.POST['date']
    emplo_schedu = Emplo_Schedu.objects.get(scheduling__date=date, employee__registration=registration)
    emplo_schedu.delete()
    return JsonResponse({'status': 'success'})
