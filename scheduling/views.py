from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from base.models import Employee, Shift, Scheduling, Emplo_Schedu, ReleasedHour, LimitHour
import json
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
from pytz import timezone


@login_required(login_url='/usuario/login')
def scheduling_employees(request):
    today = date.today()
    date_and_time_current = datetime.now()
    timezone_string = timezone('America/Sao_Paulo')
    date_and_time_sao_paulo = date_and_time_current.astimezone(timezone_string)
    time_sao_paulo_string = date_and_time_sao_paulo.strftime('%H:%M')
    user_released_hour = ReleasedHour.objects.filter(user_id=request.user.id, create_at__year=today.year,
                                                     create_at__month=today.month,
                                                     create_at__day=today.day).last()

    if user_released_hour:
        if user_released_hour.released_hour.strftime('%H:%M') > time_sao_paulo_string:
            leaders = Employee.objects.filter(leader=True, sector=request.user.userprofileinfo.sector).order_by('name')
            shifts = Shift.objects.all()
            data = {"leaders": leaders, "shifts": shifts}
            return render(request, 'scheduling_employees.html', data)
        else:
            return render(request, 'time_lock.html')
    elif "14:00" > time_sao_paulo_string:
        leaders = Employee.objects.filter(leader=True, sector=request.user.userprofileinfo.sector).order_by('name')
        shifts = Shift.objects.all()
        data = {"leaders": leaders, "shifts": shifts}
        return render(request, 'scheduling_employees.html', data)
    else:
        return render(request, 'time_lock.html')


def selected_leader(request):
    leader = Employee.objects.get(id=request.GET['lider_id'])
    employees = Employee.objects.filter(leader_name=leader.name).order_by('name')
    limit_hour = LimitHour.objects.last()
    limit_hourJson = dict(hours=limit_hour.hours)
    employees_res = []
    for employee in employees:
        json_obj = dict(name=employee.name, id=employee.id, registration=employee.registration,
                        occupation=employee.occupation, extra_hour=employee.extra_hour)
        employees_res.append(json_obj)

    data = {
        "employees": employees_res,
        "limit_hour": limit_hourJson,
        "leader": dict(name=leader.name, occupation=leader.occupation)
    }
    return HttpResponse(json.dumps(data), content_type='application/json')


def finalize_employee_scheduling(request):
    scheduling_date = request.POST['scheduling_date']
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
            continue
        else:
            unscheduled_employees.append(registration)

    if scheduled_employees:
        response = {
            'status': 'success',
            'scheduled_employees': scheduled_employees,
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
            'status': 'success',
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
        employees = Employee.objects.filter(name__icontains=search,
                                            sector=request.user.userprofileinfo.sector).order_by('name')
        leaders_res = []
        leaders_burst_res = []
        employees_res = []
        employees_burst_res = []
        limit_hour = LimitHour.objects.last()
        for employee in employees:
            employees_json_obj = dict(name=employee.name, id=employee.id, registration=employee.registration,
                                      occupation=employee.occupation, extra_hour=employee.extra_hour,
                                      leader_name=employee.leader_name)

            if Employee.objects.filter(name=employee.leader_name):
                leader = Employee.objects.filter(name=employee.leader_name)
                leader_json_obj = dict(name=leader.first().name)

                if employee.extra_hour + 7.30 > limit_hour.hours:
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
