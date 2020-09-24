from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from base.models import Shift, Employee, Emplo_Schedu, Sector
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
import xlwt

from sistecHe import settings


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
            scheduling__date=date, scheduling__shift_id=shift_params, authorized=True)
        shifts_res = [shift.to_json() for shift in shifts_res]
    else:
        shifts_res_date = Shift.objects.all()
        shifts_res = [shift.to_json() for shift in shifts_res_date]
        emplo_schedus = Emplo_Schedu.objects.prefetch_related('employee', 'scheduling').filter(
            scheduling__date=date, authorized=True)

    leaders = []
    for emplo_schedu in emplo_schedus:
        leader = Employee.objects.filter(name=emplo_schedu.employee.leader_name).first.to_json()
        if not leader in leaders:
            leaders.append(leader)

    sectors = [sector.to_json() for sector in Sector.objects.all()]

    emplo_schedus_data = [emplo_schedu.to_json() for emplo_schedu in emplo_schedus]
    date_split = date.split('-')
    formatted_date = date_split[2] + "/" + date_split[1] + "/" + date_split[0]
    count_employees = emplo_schedus.count()

    response = {
        'emplo_schedus_data': emplo_schedus_data,
        'shifts_res': shifts_res,
        'leaders': leaders,
        'sectors': sectors,
        'date': formatted_date,
        'count_employees': count_employees,
    }
    return JsonResponse(response)


def shift_pdf(request):
    date = request.GET['data']
    shift_params = int(request.GET['turno'])

    if shift_params != 0:
        shifts_res = Shift.objects.filter(id=int(shift_params))
        emplo_schedus = Emplo_Schedu.objects.prefetch_related('employee', 'scheduling').filter(
            scheduling__date=date, scheduling__shift_id=shift_params, authorized=True)
    else:
        shifts_res = Shift.objects.all()
        emplo_schedus = Emplo_Schedu.objects.prefetch_related('employee', 'scheduling').filter(
            scheduling__date=date, authorized=True)

    leaders = []
    shifts = []
    sectors = []
    for shift in shifts_res:
        if emplo_schedus.filter(scheduling__shift=shift):
            shifts.append(shift)

    for emplo_schedu in emplo_schedus:
        leader = Employee.objects.get(name=emplo_schedu.employee.leader_name)
        if not leader in leaders:
            leaders.append(leader)

    for leader in leaders:
        sector = Sector.objects.get(id=leader.sector_id)
        if not sector in sectors:
            sectors.append(sector)

    date_split = date.split('-')
    formatted_date = date_split[2] + "/" + date_split[1] + "/" + date_split[0]

    count_employees = emplo_schedus.count()
    if shifts:
        response = {
            'emplo_schedus_data': emplo_schedus,
            'shifts_res': shifts,
            'leaders': leaders,
            'sectors': sectors,
            'date': formatted_date,
            'count_employees': count_employees,
        }
    else:
        response = {
            'error': 'Sem marcações'
        }

    html_string = render_to_string('pdf/report_shift_pdf.html', response)
    html = HTML(string=html_string)
    result = html.write_pdf(stylesheets=[
        settings.BASE_DIR + '/base/static/css/css_report/report.css',
        settings.BASE_DIR + '/static/bootstrap/css/bootstrap.min.css',
    ], )

    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_people.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response

    # pdf = render_to_pdf('pdf/report_shift_pdf.html', response)
    # return HttpResponse(pdf, content_type='application/pdf')


def generate_excel_shift(request):
    shifts = Shift.objects.all()
    date = request.GET['date']
    print(date)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="relatorio_turno' + date + '.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    for shift in shifts:
        ws = wb.add_sheet(shift.name)

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Matricula', 'Nome', 'Função', 'Líder', 'Motivo', 'Setor']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        emplo_schedus = Emplo_Schedu.objects.prefetch_related('employee', 'scheduling').filter(
            scheduling__date=date, authorized=True, scheduling__shift=shift).order_by("employee__sector","employee__leader_name","employee__name")
        rows = emplo_schedus.values_list('employee__registration', 'employee__name', 'employee__occupation',
                                         'employee__leader_name', 'scheduling__reason', 'employee__sector__name')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def report_leader(request):
    shifts = Shift.objects.all()
    data = {'shifts': shifts}
    return render(request, 'report_leader.html', data)


def leader_preview(request):
    date = request.GET['date']
    shift_params = int(request.GET['shift'])

    if shift_params != 0:
        shifts_res = Shift.objects.filter(id=int(shift_params))
        emplo_schedus = Emplo_Schedu.objects.prefetch_related('employee', 'scheduling').filter(
            scheduling__date=date, scheduling__shift_id=shift_params,
            employee__sector_id=request.user.userprofileinfo.sector_id, authorized=True)
        shifts_res = [shift.to_json() for shift in shifts_res]
    else:
        shifts_res_date = Shift.objects.all()
        shifts_res = [shift.to_json() for shift in shifts_res_date]
        emplo_schedus = Emplo_Schedu.objects.prefetch_related('employee', 'scheduling').filter(
            scheduling__date=date, employee__sector_id=request.user.userprofileinfo.sector_id, authorized=True)

    leaders = []
    for emplo_schedu in emplo_schedus:
        leader = Employee.objects.filter(name=emplo_schedu.employee.leader_name).first.to_json()
        if not leader in leaders:
            leaders.append(leader)

    emplo_schedus_data = [emplo_schedu.to_json() for emplo_schedu in emplo_schedus]
    date_split = date.split('-')
    formatted_date = date_split[2] + "/" + date_split[1] + "/" + date_split[0]
    count_employees = emplo_schedus.count()
    response = {
        'emplo_schedus_data': emplo_schedus_data,
        'shifts_res': shifts_res,
        'leaders': leaders,
        'date': formatted_date,
        'count_employees': count_employees,
    }
    return JsonResponse(response)


def leader_pdf(request):
    date = request.GET['data']
    shift_params = int(request.GET['turno'])

    if shift_params != 0:
        shifts_res = Shift.objects.filter(id=int(shift_params))
        emplo_schedus = Emplo_Schedu.objects.prefetch_related('employee', 'scheduling').filter(
            scheduling__date=date, scheduling__shift_id=shift_params,
            employee__sector_id=request.user.userprofileinfo.sector_id, authorized=True)
    else:
        shifts_res = Shift.objects.all()
        emplo_schedus = Emplo_Schedu.objects.prefetch_related('employee', 'scheduling').filter(
            scheduling__date=date, employee__sector_id=request.user.userprofileinfo.sector_id, authorized=True)

    leaders = []
    shifts = []
    for shift in shifts_res:
        if emplo_schedus.filter(scheduling__shift=shift):
            shifts.append(shift)

    for emplo_schedu in emplo_schedus:
        leader = Employee.objects.get(name=emplo_schedu.employee.leader_name)
        if not leader in leaders:
            leaders.append(leader)

    date_split = date.split('-')
    formatted_date = date_split[2] + "/" + date_split[1] + "/" + date_split[0]

    count_employees = emplo_schedus.count()
    if shifts:
        response = {
            'emplo_schedus_data': emplo_schedus,
            'shifts_res': shifts,
            'leaders': leaders,
            'date': formatted_date,
            'count_employees': count_employees,
        }
    else:
        response = {
            'error': 'Sem marcações'
        }

    html_string = render_to_string('pdf/report_leader_pdf.html', response)
    html = HTML(string=html_string)
    result = html.write_pdf(stylesheets=[
        settings.BASE_DIR + '/base/static/css/css_report/report.css',
        settings.BASE_DIR + '/static/bootstrap/css/bootstrap.min.css',
    ], )

    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_people.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response


def generate_excel_leader(request):
    shifts = Shift.objects.all()
    date = request.GET['date']
    print(date)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="relatorio_lider' + date + '.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    for shift in shifts:
        ws = wb.add_sheet(shift.name)

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Matricula', 'Nome', 'Função', 'Líder', 'Motivo']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        emplo_schedus = Emplo_Schedu.objects.prefetch_related('employee', 'scheduling').filter(
            scheduling__date=date, scheduling__shift=shift,
            employee__sector_id=request.user.userprofileinfo.sector_id, authorized=True).order_by("employee__leader_name","employee__name")
        rows = emplo_schedus.values_list('employee__registration', 'employee__name', 'employee__occupation',
                                         'employee__leader_name', 'scheduling__reason')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response