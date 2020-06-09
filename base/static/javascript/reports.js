$("#form_report_shift").submit(function (event) {
    event.preventDefault()
    let date = $("[name=date]").val()
    let shift = $("[name=shift]").val()
    page = $('.reports_info')
    console.log(page)
    $.ajax({
        url: 'por_turno/preview',
        data: {'date': date, 'shift': shift},
        dateType: 'json',
        success: function (data) {
            for (var x = 0; x <= data['shifts_res'].length; x++) {
                if (shi_is_present_emp_sch(data['shifts_res'][x]['id'], data['emplo_schedus_data'])) {
                    page.append('<h1 class="display-4 text-center turnoTitle">' + data['shifts_res'][x]['name'] + '</h1>')
                }
                for (var y = 0; y <= data['sectors'].length; y++) {
                    if (sec_is_present_emp_sch(data['sectors'][y]['id'], data['emplo_schedus_data'])) {
                        page.append('<h2 class="fontSetorGE">' + data['sectors'][y]['name'] + '</h2>')
                    }
                    for (var a = 0; a <= data['leaders'].length; a++) {
                        if (data['leaders'][a]['sector']['id'] === data['sectors'][y]['id']) {
                            page.append('<h1 class="text-center text-muted">' + data['leaders'][a]['name'] + '</h1>')
                            page.append('<table class="table fontTableGE table_reports_info">\n' +
                                '                    <thead>\n' +
                                '                    <tr>\n' +
                                '                      <th>Matricula</th>\n' +
                                '                      <th>Funcionário</th>\n' +
                                '                      <th>Motivo</th>\n' +
                                '                      <th>HE Previsto</th>\n' +
                                '                    </tr>\n' +
                                '                    </thead>\n' +
                                '                    <tbody>')
                        }
                        for (var z = 0; z < data['emplo_schedus_data'].length; z++) {
                            var table = $('.table_reports_info tbody')
                            if (data['emplo_schedus_data'][z]['employee']['leader_name'] == data['leaders'][a]['name']) {
                                table.append('<tr>\n' +
                                    '                        <td>' + data['emplo_schedus_data'][z]['employee']['registration'] + '</td>\n' +
                                    '                        <td>' + data['emplo_schedus_data'][z]['employee']['name'] + '</td>\n' +
                                    '                        <td>' + data['emplo_schedus_data'][z]['scheduling']['reason'] + '</td>\n' +
                                    '                        <td>' + data['emplo_schedus_data'][z]['employee']['extra_hour'] + '</td>\n' +
                                    '                      </tr>')
                            }
                        }
                    }
                }
            }
        }
    })
})

function shi_is_present_emp_sch(dic1, dic2) {
    for (var y = 0; y <= dic2.length; y++) {
        try {
            if (dic2[y]['scheduling']['shift']['id'] == dic1) {
                return true
            }
        } catch (e) {
            return false
        }
    }
}

function sec_is_present_emp_sch(dic1, dic2) {
    for (var y = 0; y <= dic2.length; y++) {
        try {
            if (dic2[y]['scheduling']['sector']['id'] == dic1) {
                return true
            }
        } catch (e) {
            return false
        }
    }
}