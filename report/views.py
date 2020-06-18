from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from base.models import Shift, Employee, Emplo_Schedu, Sector
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile


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
        leader = Employee.objects.get(name=emplo_schedu.employee.leader_name).to_json()
        if not leader in leaders:
            leaders.append(leader)

    sectors = [sector.to_json() for sector in Sector.objects.all()]

    emplo_schedus_data = [emplo_schedu.to_json() for emplo_schedu in emplo_schedus]
    date_split = date.split('-')
    formatted_date = date_split[2] + "/" + date_split[1] + "/" + date_split[0]
    response = {
        'emplo_schedus_data': emplo_schedus_data,
        'shifts_res': shifts_res,
        'leaders': leaders,
        'sectors': sectors,
        'date': formatted_date,
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
    result = html.write_pdf()

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
        leader = Employee.objects.get(name=emplo_schedu.employee.leader_name).to_json()
        if not leader in leaders:
            leaders.append(leader)

    emplo_schedus_data = [emplo_schedu.to_json() for emplo_schedu in emplo_schedus]
    date_split = date.split('-')
    formatted_date = date_split[2] + "/" + date_split[1] + "/" + date_split[0]
    response = {
        'emplo_schedus_data': emplo_schedus_data,
        'shifts_res': shifts_res,
        'leaders': leaders,
        'date': formatted_date,
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
    result = html.write_pdf()

    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_people.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response
