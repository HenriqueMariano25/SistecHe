from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
import xlrd
import pandas as pd
from xlrd.timemachine import xrange
import locale
from datetime import datetime

from base.models import SubSector, Employee, Sector, ImportHistory


def employees(request):
    if request.user.is_authenticated:
        employees = Employee.objects.all().order_by('name')
        import_history = ImportHistory.objects.filter(type="employees").last()
        if import_history:
            import_history = import_history.created_at
        if request.method == 'POST':
            search = request.POST['search']
            if 'search' in request.POST:
                employees = employees.filter(name__icontains=search)

        data = {'employees': employees,
                'sectors': Sector.objects.all(),
                'import_history': import_history,
                'import_history_create_at': import_history}
        return render(request, 'employees.html', data)
    else:
        return redirect('login')


def update_employees(request):
    import_history = ImportHistory(type="employees", made_by=request.user,
                                   created_at=timezone.localtime(timezone.now()).strftime('%d/%m/%Y - %H:%M'))
    import_history.save()
    if request.method == 'POST':
        excel = request.FILES['excel']
        datas = pd.read_excel(excel.file)
        for data in datas.index:
            registration = str(datas['Matricula'][data])[-8:]
            demission_date = datas['Data de demissao (DD/MM/AAAA)'][data]
            name = datas['Funcionario'][data]
            leader_name = datas['Lider equipe'][data]
            admission_date = datas['Data de admissao (DD/MM/AAAA)'][data]
            occupation = datas['Descricao funcao'][data]
            manager = datas['Nome gestor'][data]
            if type(demission_date) == str:
                demission_date = demission_date.strip()

            if type(demission_date) == float:
                demission_date = ""

            if registration != " ":
                employee = Employee.objects.filter(registration=registration).first()
                if not employee is None and demission_date != "":
                    employee.delete()
                    continue

                if not demission_date == "":
                    continue

                subsector = str(datas['Empresa'][data]).split('-')[0]  # print(SubSector.objects.filter(name=subsector))
                if SubSector.objects.filter(name=subsector).exists():
                    subSector = SubSector.objects.filter(name=subsector).first()
                else:
                    subSector = SubSector(name=subsector)
                    subSector.save()

                if not employee == None:
                    if not employee.name == name and employee.occupation == occupation and \
                            employee.admission_date == admission_date and employee.manager == manager and \
                            employee.leader_name == leader_name and employee.sub_sector == subSector:
                        employee.name = name
                        employee.occupation = occupation
                        employee.leader_name = leader_name
                        employee.admission_date = admission_date
                        employee.manager = manager
                        employee.sub_sector = subSector
                        employee.save()
                else:
                    employee = Employee(name=name, occupation=occupation, registration=registration,
                                        admission_date=admission_date, manager=manager,
                                        leader_name=leader_name, sub_sector=subSector)
                    employee.save()
        return redirect('employees')


def update_employees_leader(request):
    registration = request.GET['registration']
    situation = request.GET['situation']
    employee = Employee.objects.get(registration=registration)
    if situation == 'yes':
        employee.leader = True
    elif situation == 'no':
        employee.leader = False
    if employee.save:
        employee.save()
        data = {
            'result': 'OK'
        }
    else:
        data = {
            'result': 'Fail'
        }
    return JsonResponse(data)


def update_employees_sector(request):
    registration = request.POST['employee_registration']
    id_sector = request.POST['id_sector']
    employee = Employee.objects.get(registration=registration)
    employee.sector_id = id_sector
    if employee.save:
        employee.save()
        return JsonResponse({'result': 'OK'})
    else:
        return JsonResponse({'result': 'Fail'})


def extra_hour(request):
    if request.user.is_authenticated:
        employees = Employee.objects.all().order_by('-extra_hour')
        import_history = ImportHistory.objects.filter(type="extra_hour").last()
        if import_history:
            import_history = import_history.created_at
        if request.method == "POST":
            search = request.POST['search']
            if 'search' in request.POST:
                employees = employees.filter(name__icontains=search)
        data = {'employees': employees,
                'import_history': import_history,
                'import_history_create_at': import_history}
        return render(request, 'extra_hour.html', data)


def update_extra_hour(request):
    import_history = ImportHistory(type="extra_hour", made_by=request.user,
                                   created_at=timezone.localtime(timezone.now()).strftime('%d/%m/%Y - %H:%M'))
    import_history.save()
    if request.method == 'POST':
        excel = request.FILES['excel']
        workbook = xlrd.open_workbook(file_contents=excel.read())
        sheet = workbook.sheet_by_index(1)
        for row_num in xrange(sheet.nrows):
            row = sheet.row_values(row_num)
            if row[0] == "" or row[0] == "MATRICULA":
                continue
            registration = int(row[0])
            extra_hour = round(row[4], 1)
            employee = Employee.objects.filter(registration=registration).first()
            if not employee:
                continue
            employee.extra_hour = extra_hour
            if employee.save:
                employee.save()
        return redirect('extra_hour')


def reset_extra_hours(request):
    if request.method == 'POST':
        reset_all_employees_extra_time()
        return redirect('extra_hour')


def reset_all_employees_extra_time():
    Employee.objects.all().update(extra_hour=0.0)
    return None
