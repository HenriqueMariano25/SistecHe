from __future__ import unicode_literals

from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
import xlrd
from xlrd.timemachine import xrange
from datetime import date
from django.core.paginator import Paginator

from base.models import SubSector, Employee, Sector, ImportHistory, ReleasedHour, LimitHour


def employees(request):
    if request.user.is_authenticated:

        employees_list = Employee.objects.all().order_by('name')

        paginator = Paginator(employees_list, 20)
        page = request.GET.get('page')
        employees = paginator.get_page(page)

        import_history = ImportHistory.objects.filter(type="employees").last()
        if request.method == 'POST':
            search = request.POST['search']
            if 'search' in request.POST:
                employees = employees_list.filter(name__icontains=search)

        data = {'employees': employees,
                'sectors': Sector.objects.all(),
                'import_history': import_history
                }
        return render(request, 'employees.html', data)
    else:
        return redirect('login')


def update_employees(request):
    SECTORS = {
        'ADMINISTRACAO': Sector.objects.get(name="Administração"),
        'PLANEJAMENTO': Sector.objects.get(name="Planejamento"),
        'PRODUCAO': Sector.objects.get(name="Produção"),
        'CONSTRUCAO & MONTAGEM': Sector.objects.get(name="Produção"),
        'SMSRS': Sector.objects.get(name="SMSRS"),
        'QUALIDADE': Sector.objects.get(name="Qualidade"),
        'ENGENHARIA': Sector.objects.get(name="Engenharia"),
        'COMISSIONAMENTO': Sector.objects.get(name="Comissionamento"),
        'SUPRIMENTOS OBRA': Sector.objects.get(name="Suprimentos"),
        'SUPRIMENTOS SP': Sector.objects.get(name="Suprimentos"),
        'PRESERVAÇÃO': Sector.objects.get(name="Suprimentos"),
        'DIRETORIA DE CONTRATO': Sector.objects.get(name="Diretoria de Contrato"),
        'GERENCIA ADCON': Sector.objects.get(name="Administração Contratual"),
    }

    excel = request.FILES['excel']
    workbook = xlrd.open_workbook(file_contents=excel.read())
    sheet = workbook.sheet_by_index(0)
    for row_num in xrange(sheet.nrows):
        row = sheet.row_values(row_num)
        if row[0] == "" or row[0] == "Id reduzido":
            continue

        demission_date = row[4]

        if type(demission_date) == str:
            demission_date = demission_date.strip()

        if type(demission_date) == float:
            demission_date = ""

        if not demission_date == "":
            continue

        occupation = row[5]

        if occupation == "JOVEM APRENDIZ":
            continue

        if row[12] != "":
            sector = row[12].split('-')[1].strip()
            sector = SECTORS[sector]
        else:
            continue

        registration = str(row[2])[-8:]
        demission_date = row[4]
        name = row[1]
        leader_name = row[8]
        admission_date = date.fromordinal(693594 + int(row[3]))
        manager = row[9]

        if registration != " ":
            employee = Employee.objects.filter(registration=registration).first()
            if not employee is None and demission_date != "":
                employee.delete()
                continue

            subsector = str(row[10]).split('-')[0]
            sub = SubSector.objects.filter(name=subsector)
            if sub.exists():
                subSector = sub.first()
            else:
                subSector = SubSector(name=subsector)
                subSector.save()
            if not employee is None:
                if not employee.sector == sector or employee.name == name or employee.occupation == occupation or \
                        employee.admission_date == admission_date or employee.manager == manager or \
                        employee.leader_name == leader_name or employee.sub_sector == subSector:
                    employee.name = name
                    employee.occupation = occupation
                    employee.leader_name = leader_name
                    employee.admission_date = admission_date
                    employee.manager = manager
                    employee.sub_sector = subSector
                    employee.sector = sector
                    if employee.save:
                        employee.save()
            else:
                employee = Employee(name=name, occupation=occupation, registration=registration,
                                    admission_date=admission_date, manager=manager,
                                    leader_name=leader_name, sub_sector=subSector, sector=sector)
                if employee.save:
                    employee.save()

    for row_num in xrange(sheet.nrows):
        row = sheet.row_values(row_num)
        if row[0] == "" or row[0] == "Id reduzido":
            continue
        leader_name = row[8]
        leader = Employee.objects.filter(name=leader_name).first()
        if leader:
            leader.leader = True
            leader.save()

    import_history = ImportHistory(type="employees", made_by=request.user,
                                   created_at=timezone.localtime(timezone.now()).strftime('%d/%m/%Y - %H:%M'))
    import_history.save()

    return redirect('employees')


# def validate_leaders(request):
#     excel = request.FILES['excel']
#     workbook = xlrd.open_workbook(file_contents=excel.read())
#     sheet = workbook.sheet_by_index(0)
#     for row_num in xrange(sheet.nrows):
#         row = sheet.row_values(row_num)
#         if row[0] == "" or row[0] == "Id reduzido":
#             continue
#         leader_name = row[8]
#         leader = Employee.objects.filter(name=leader_name).first()
#         if leader:
#             leader.leader = True
#             leader.save()
#     pass


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
        employees_list = Employee.objects.all().order_by('-extra_hour')

        paginator = Paginator(employees_list, 20)
        page = request.GET.get('page')
        employees = paginator.get_page(page)

        import_history = ImportHistory.objects.filter(type="extra_hour").last()
        limit_hour = LimitHour.objects.last()
        if request.method == "POST":
            search = request.POST['search']
            if 'search' in request.POST:
                employees = employees_list.filter(name__icontains=search)
        data = {'employees': employees,
                'import_history': import_history,
                'limit_hour': limit_hour,
                }
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


def extra_hour_limit(request):
    today = date.today()
    users = User.objects.prefetch_related('releasedhours').filter(is_superuser=False).order_by('first_name')
    # releasedhours__create_at__year=today.year,
    # releasedhours__create_at__month=today.month,
    # releasedhours__create_at__day=today.day)

    released_hour = ReleasedHour.objects.filter(create_at__year=today.year, create_at__month=today.month,
                                                create_at__day=today.day).order_by('user', '-create_at').distinct(
        'user')
    if request.method == "POST":
        search = request.POST['search']
        if 'search' in request.POST:
            users = users.filter(username__icontains=search)

    data = {
        'users': users,
        'released_hour': released_hour
    }
    return render(request, 'extra_hour_limit.html', data)


def update_extra_hour_limit(request):
    if request.method == 'POST':
        released_hour = request.POST['time_released']
        reason = request.POST['reason']
        user = get_object_or_404(User, id=request.POST['user'])
        hour = ReleasedHour(released_hour=released_hour, reason=reason, user=user, made_by=request.user.username,
                            create_at=timezone.localtime(timezone.now()))
        if hour.save:
            hour.save()
        return redirect('extra_hour_limit')


def update_extra_hour_month(request):
    if request.method == "POST":
        hours = request.POST['hours']
        print(hours)
        limit = LimitHour(hours=hours, made_by=request.user, create_at=timezone.localtime(timezone.now()))
        if limit.save:
            limit.save()
        return redirect('extra_hour')


def extra_hour_limit_sector(request):
    sectors = Sector.objects.all().order_by("name")
    data = {
        'sectors':sectors
    }
    return render(request, 'extra_hour_limit_sector.html', data)


def update_extra_hour_limit_sector(request):
    if request.method == "POST":
        hours = request.POST['hours']
        sector_id = request.POST['sector_id']
        sector = Sector.objects.get(id=sector_id)
        sector.time_limit=hours
        sector.save()
    return redirect('extra_hour_limit_sector')