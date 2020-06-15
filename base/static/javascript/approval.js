$("#form_director_list").submit(function (event) {
    event.preventDefault()
    var date = $('[name=date]').val()
    var shift = $('[name=shift]').val()
    var sector = $('[name=sector]').val()
    page = $('.director_list')
    $.ajax({
        url: 'diretor/lista',
        data: {'date': date, 'shift': shift, 'sector':sector},
        dateType: 'json',
        success: function (data) {
            const shifts = data.shifts
            const sectors = data.sectors
            const leaders = data.leaders
            const emplo_schedus = data.emplo_schedus
            console.log("teste")
            page.children().remove()
            page.append('<form action="" method="post" id="approve_schedule">' +
            '<div class="row bg-dark">' +
                '<div class="bg-danger">' +
                '<h1 class="dateReport text-right">' + date + '</h1> ' +
                '</div>' +
                '</div>')
            for (var x = 0; x < shifts.length; x++) {
                if (emplo_schedus.find(emplo_schedus => emplo_schedus.scheduling.shift.id === shifts[x].id)) {
                    page.append('<h1 class="display-4 text-center turnoTitle">' + shifts[x].name + '</h1>')
                }
                for (y = 0; y < sectors.length; y++) {
                    if (emplo_schedus.find(emplo_schedus => emplo_schedus.employee.sector.id === sectors[y].id && emplo_schedus.scheduling.shift.id === shifts[x].id)) {
                        page.append('<h2 class="fontSetorGE">' + sectors[y].name + '</h2>')
                    }
                    leaders_sector = leaders.filter(leaders => leaders.sector.id === sectors[y].id)
                    $.each(leaders_sector, function (key, value) {
                        if (emplo_schedus.find(emplo_schedus => emplo_schedus.employee.leader_name === value.name && emplo_schedus.scheduling.shift.id === shifts[x].id)) {
                            page.append('<h1 class="text-center text-muted">' + value.name + '</h1>')
                            var tr = ""
                            var table = '<table class="table fontTableGE" id="table_reports_info">\n' +
                                '  <thead class="theadAll">\n' +
                                '      <tr>\n' +
                                '          <th>Che</th>\n' +
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
                                if(value.authorized === true){
                                    checkbox = '<input id="check_leader" type="checkbox" value="teste" checked on_click="is_authorized()">'
                                }else{
                                    checkbox = '<input id="check_leader" type="checkbox" value="teste" on_click="is_authorized()>'
                                }
                                tr = tr + '<tr>\n' +
                                    '  <td>'+checkbox+'</td>\n' +
                                    '  <td>' + value.employee.registration + '</td>\n' +
                                    '  <td>' + value.employee.name + '</td>\n' +
                                    '  <td>' + value.employee.occupation + '</td>\n' +
                                    '  <td>' + value.scheduling.reason + '</td>\n' +
                                    '  <td>' + value.employee.extra_hour + '</td>\n' +
                                    '</tr>'
                            })
                            page.append(table + tr)
                            approve_schedule = '<div style="position:fixed ">'+
                                             '<input type="submit">'+
                                                 '</div>'+
                                                 '</form>'
                            page.append(approve_schedule)
                        }
                    })
                }
            }

        }
    })
})
$("#approve_schedule").submit(function () {
        alert("teste")
    })