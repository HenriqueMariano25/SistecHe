$("#form_report_shift").submit(function (event) {
    event.preventDefault()
    let date_input = $("[name=date]").val()
    let shift_input = $("[name=shift]").val()
    page = $('.reports_info')
    $.ajax({
        url: 'por_turno/preview',
        data: {'date': date_input, 'shift': shift_input},
        dateType: 'json',
        success: function (data) {
            const leaders = data.leaders
            const emplo_schedus = data.emplo_schedus_data
            const shifts = data.shifts_res
            const sectors = data.sectors
            const date = data.date
            const count = data.count_employees
            page.children().remove()
            page.append('<div class="container ">' +
                '<div class="row justify-content-center">' +
                '<div class="col-4 mb-4">' +
                '<a target="_blank" class="btn btn-success btn-block mb-3" style="font-size: 20px" href="por_turno/pdf?data=' + date_input + '&turno=' + shift_input + '">Gerar PDF</a>' +
                '<a href="por_turno/excel?date='+date_input+'">Gerar excel</a>' +
                '</div>' +
                '</div>' +
                '</div>')
            page.append('<div class="row">' +
                '<div class="col-3">' +
                '<img src="https://i.pinimg.com/originals/88/dd/e1/88dde1160aaebf6bfe42750b87afe11c.png" class="soonReport">' +
                '</div>' +
                '<div class="col-6">' +
                '<h1 class="text-center textTitleReport"><strong>RELATÓRIO POR TURNO | AG</strong></h1>' +
                '</div>' +
                '<div class="col-3">' +
                '<h1 class="dateReport text-right ">' + date + '</h1> ' +
                '<h3>Funcionairo agendados:'+count+'</h3>'+
                '</div>' +
                '</div>')
            for (var x = 0; x < data['shifts_res'].length; x++) {
                if (data.emplo_schedus_data.find(emplo_schedus => emplo_schedus.scheduling.shift.id === data.shifts_res[x].id)) {
                    page.append('<h1 class="display-4 text-center mt-5 turnTitle ">' + data['shifts_res'][x]['name'] + '</h1>')
                }

                for (y = 0; y < data['sectors'].length; y++) {
                    if (emplo_schedus.find(emplo_schedus => emplo_schedus.employee.sector.id === sectors[y].id && emplo_schedus.scheduling.shift.id === shifts[x].id)) {
                        page.append('<h2>' + data['sectors'][y]['name'] + '</h2>')
                    }
                    leaders_sector = leaders.filter(leaders => leaders.sector.id === sectors[y].id)
                    $.each(leaders_sector, function (key, value) {
                        if (emplo_schedus.find(emplo_schedus => emplo_schedus.employee.leader_name === value.name && emplo_schedus.scheduling.shift.id === shifts[x].id)) {
                            page.append('<h1 class="text-center text-muted leaderTitle mt-5 mb-4">' + value.name + '</h1>')
                            var tr = ""
                            var table = '<table class="table fontTableGE" id="table_reports_info">\n' +
                                '  <thead class="theadAll">\n' +
                                '      <tr>\n' +
                                '          <th>Matricula</th>\n' +
                                '          <th>Funcionário</th>\n' +
                                '          <th>Função</th>\n' +
                                '          <th>Motivo</th>\n' +
                                '          <th>HE Previsto</th>\n' +
                                '       </tr>\n' +
                                '   </thead>\n' +
                                '<tbody>'
                            employees_leaders = emplo_schedus.filter(emplo_schedus => emplo_schedus.employee.leader_name === value.name)
                            $.each(employees_leaders, function (key, value) {
                                tr = tr + '<tr>\n' +
                                    '  <td>' + value.employee.registration + '</td>\n' +
                                    '  <td>' + value.employee.name + '</td>\n' +
                                    '  <td>' + value.employee.occupation + '</td>\n' +
                                    '  <td>' + value.scheduling.reason + '</td>\n' +
                                    '  <td>' + value.employee.extra_hour + '</td>\n' +
                                    '</tr>'
                            })
                            page.append(table + tr)
                        }
                    })
                }
            }
        }
    })
})

$("#form_report_leader").submit(function (event) {
    event.preventDefault()
    let date_input = $("[name=date]").val()
    let shift_input = $("[name=shift]").val()
    page = $('.reports_info')
    $.ajax({
        url: 'por_lider/preview',
        data: {'date': date_input, 'shift': shift_input},
        dateType: 'json',
        success: function (data) {
            const leaders = data.leaders
            const emplo_schedus = data.emplo_schedus_data
            const shifts = data.shifts_res
            const date = data.date
            const count = data.count_employees
            page.children().remove()
            page.append('<div class="container ">' +
                '<div class="row justify-content-center">' +
                '<div class="col-4 mb-4">' +
                '<a target="_blank" class="btn btn-success btn-block mb-3" style="font-size: 20px" href="por_lider/pdf?data=' + date_input + '&turno=' + shift_input + '">Gerar PDF</a>' +
                '<a href="por_lider/excel?date='+date_input+'">Gerar excel</a>' +
                '</div>' +
                '</div>' +
                '</div>')
            page.append('<div class="row ">' +
                '<div class="col-3">' +
                '<img src="https://i.pinimg.com/originals/88/dd/e1/88dde1160aaebf6bfe42750b87afe11c.png" class="soonReport">' +
                '</div>' +
                '<div class="col-6">' +
                '<h1 class="text-center textTitleReport"><strong>RELATÓRIO POR LIDER | AG</strong></h1>' +
                '</div>' +
                '<div class="col-3">' +
                '<h1 class="dateReport text-right ">' + date + '</h1>' +
                '<h3>Funcionairo agendados:'+count+'</h3>'+
                '</div>' +
                '</div>')
            for (var x = 0; x < shifts.length; x++) {
                if (emplo_schedus.find(emplo_schedus => emplo_schedus.scheduling.shift.id === shifts[x].id)) {
                    page.append('<h1 class="display-4 text-center mt-5 turnTitle">' + shifts[x].name + '</h1>')
                    $.each(leaders, function (key, value) {
                        if (emplo_schedus.find(emplo_schedus => emplo_schedus.employee.leader_name === value.name && emplo_schedus.scheduling.shift.id === shifts[x].id)) {
                            page.append('<h1 class="text-center text-muted leaderTitle mt-5 mb-4">' + value.name + '</h1>')
                            var tr = ""
                            var table = '<table class="table fontTableGE" id="table_reports_info">\n' +
                                '  <thead class="theadAll">\n' +
                                '      <tr>\n' +
                                '          <th>Matricula</th>\n' +
                                '          <th>Funcionário</th>\n' +
                                '          <th>Função</th>\n' +
                                '          <th>Motivo</th>\n' +
                                '          <th>HE Previsto</th>\n' +
                                '       </tr>\n' +
                                '   </thead>\n' +
                                '<tbody>'
                            employees_leaders = emplo_schedus.filter(emplo_schedus => emplo_schedus.employee.leader_name === value.name)
                            $.each(employees_leaders, function (key, value) {
                                tr = tr + '<tr>\n' +
                                    '  <td>' + value.employee.registration + '</td>\n' +
                                    '  <td>' + value.employee.name + '</td>\n' +
                                    '  <td>' + value.employee.occupation + '</td>\n' +
                                    '  <td>' + value.scheduling.reason + '</td>\n' +
                                    '  <td>' + value.employee.extra_hour + '</td>\n' +
                                    '</tr>'
                            })
                            page.append(table + tr)
                        }
                    })
                }
            }
        }
    })
})