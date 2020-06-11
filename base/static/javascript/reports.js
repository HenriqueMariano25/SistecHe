$("#form_report_shift").submit(function (event) {
    event.preventDefault()
    let date = $("[name=date]").val()
    let shift = $("[name=shift]").val()
    page = $('.reports_info')
    $.ajax({
        url: 'por_turno/preview',
        data: {'date': date, 'shift': shift},
        dateType: 'json',
        success: function (data) {
            const leaders = data.leaders
            const emplo_schedus = data.emplo_schedus_data
            const shifts = data.shifts_res
            const sectors = data.sectors
            const date = data.date
            console.log(data)
            page.children().remove()
            page.append('<h1>'+date+'</h1>')
            for (var x = 0; x < data['shifts_res'].length; x++) {
                if (data.emplo_schedus_data.find(emplo_schedus => emplo_schedus.scheduling.shift.id === data.shifts_res[x].id)) {
                    page.append('<h1 class="display-4 text-center turnoTitle">' + data['shifts_res'][x]['name'] + '</h1>')
                }

                for (y = 0; y < data['sectors'].length; y++) {
                    if (emplo_schedus.find(emplo_schedus => emplo_schedus.employee.sector.id === sectors[y].id && emplo_schedus.scheduling.shift.id === shifts[x].id)) {
                        page.append('<h2 class="fontSetorGE">' + data['sectors'][y]['name'] + '</h2>')
                    }
                    leaders_sector = leaders.filter(leaders => leaders.sector.id === sectors[y].id)
                    $.each(leaders_sector, function (key, value) {
                        if (emplo_schedus.find(emplo_schedus => emplo_schedus.employee.leader_name === value.name && emplo_schedus.scheduling.shift.id === shifts[x].id)) {
                            page.append('<h1 class="text-center text-muted">' + value.name + '</h1>')
                            var tr = ""
                            var table = '<table class="table fontTableGE" id="table_reports_info">\n' +
                                '  <thead>\n' +
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