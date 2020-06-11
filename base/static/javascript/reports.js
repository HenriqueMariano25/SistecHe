$("#form_report_shift").submit(function (event) {
    event.preventDefault()
    let date = $("[name=date]").val()
    let shift = $("[name=shift]").val()
    page = $('.reports_info')
    // console.log(page)
    $.ajax({
        url: 'por_turno/preview',
        data: {'date': date, 'shift': shift},
        dateType: 'json',
        success: function (data) {
            console.log(data)
            const leaders = data.leaders
            const emplo_schedus = data.emplo_schedus_data
            const shifts = data.shifts_res
            const sectors = data.sectors
            const date = data.date
            // const
            // console.log(data.sectors)
            // teste = JSON.parse(data.sectors)
            // console.log(teste)
            // console.log(Object.values(data.emplo_schedus_data))
            // function isPresent(emp_sch,shift) {
            //     return emp_sch.scheduling.shift.id === shift;
            // }
            // const result = data.emplo_schedus_data.find(emplo_schedus => emplo_schedus.scheduling.shift.id === 3)

            // console.log(result);
            page.children().remove()
            page.append('<h1>'+date+'</h1>')
            console.log(data['date'])
            for (var x = 0; x < data['shifts_res'].length; x++) {
                // if (shi_is_present_emp_sch(data['shifts_res'][x]['id'], data['emplo_schedus_data'])) {
                //     page.append('<h1 class="display-4 text-center turnoTitle">' + data['shifts_res'][x]['name'] + '</h1>')
                // }
                if (data.emplo_schedus_data.find(emplo_schedus => emplo_schedus.scheduling.shift.id === data.shifts_res[x].id)) {
                    page.append('<h1 class="display-4 text-center turnoTitle">' + data['shifts_res'][x]['name'] + '</h1>')
                    // console.log(data['shifts_res'][x]['name'])
                }

                for (y = 0; y < data['sectors'].length; y++) {
                    // console.log(emplo_schedus.find(emplo_schedus => emplo_schedus.employee.sector.id === sectors[y].id && emplo_schedus.scheduling.shift.id === shifts[x].id))
                    // console.log(sectors[y])
                    if (emplo_schedus.find(emplo_schedus => emplo_schedus.employee.sector.id === sectors[y].id && emplo_schedus.scheduling.shift.id === shifts[x].id)) {
                        page.append('<h2 class="fontSetorGE">' + data['sectors'][y]['name'] + '</h2>')
                    }
                    leaders_sector = leaders.filter(leaders => leaders.sector.id === sectors[y].id)
                    // console.log(leaders_sector)
                    $.each(leaders_sector, function (key, value) {
                        if (emplo_schedus.find(emplo_schedus => emplo_schedus.employee.leader_name === value.name && emplo_schedus.scheduling.shift.id === shifts[x].id)) {
                            // console.log(value)
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
                                // if (value.employee.leader_name === value.name && value.scheduling.shift.id === shifts[x].id && value.employee.sector.id === sectors[y].id) {
                                // console.log(value.employee.name)

                                tr = tr + '<tr>\n' +
                                    '  <td>' + value.employee.registration + '</td>\n' +
                                    '  <td>' + value.employee.name + '</td>\n' +
                                    '  <td>' + value.employee.occupation + '</td>\n' +
                                    '  <td>' + value.scheduling.reason + '</td>\n' +
                                    '  <td>' + value.employee.extra_hour + '</td>\n' +
                                    '</tr>'
                                // }
                            })
                            page.append(table + tr)
                        }
                    })
                    // if
                    // page.append('<div id="teste"></div>')
                    // if (data['leaders'][a]['sector']['id'] === data['sectors'][y]['id'] && emplo_schedus.find(emplo_schedus => emplo_schedus.employee.leader_name === leaders[a].name && emplo_schedus.scheduling.shift.id === shifts[x].id)) {
                    //     console.log(leaders[a].name)
                    //     page.append('<h1 class="text-center text-muted">' + data['leaders'][a]['name'] + '</h1>')
                    //     var table = '<table class="table fontTableGE" id="table_reports_info">\n' +
                    //         '                    <thead>\n' +
                    //         '                    <tr>\n' +
                    //         '                      <th>Matricula</th>\n' +
                    //         '                      <th>Funcionário</th>\n' +
                    //         '                      <th>Motivo</th>\n' +
                    //         '                      <th>HE Previsto</th>\n' +
                    //         '                    </tr>\n' +
                    //         '                    </thead>\n' +
                    //         '                    <tbody>'
                    // }

                    // var table = $('#table_reports_info tbody')
                    // var table = $('#table_reports_info tbody')
                    // var oi = "oi" << "tchau"
                    var tr = ""
                    $.each(employees_leaders, function (key, value) {

                        // if (value.employee.leader_name === leaders[a].name && value.scheduling.shift.id === shifts[x].id && value.employee.sector.id === sectors[y].id) {
                        //     console.log(value.employee.name)
                        //      tr = tr + '<tr>\n' +
                        //         '                        <td>' + value.employee.registration + '</td>\n' +
                        //         '                        <td>' + value.employee.name + '</td>\n' +
                        //         '                        <td>' + value.scheduling.reason + '</td>\n' +
                        //         '                        <td>' + value.employee.extra_hour + '</td>\n' +
                        //         '                      </tr>'
                        // }
                    })
                    // console.log(table)
                    // console.log(tr)
                    // if(tr !== undefined && table !== undefined){
                    //     page.append(table + tr +'</tbody></table>')
                    // }


                    // for (var z = 0; z < data['emplo_schedus_data'].length; z++) {
                    //     // console.log(emplo_schedus.filter(emplo_schedus => emplo_schedus.employee.leader_name === leaders[a].name))
                    //     // emplo_schedus.find(emplo_schedus => emplo_schedus.employee.leader_name === leaders[a].name
                    //     if (emplo_schedus[z].employee.leader_name === leaders[a].name && emplo_schedus[z].scheduling.shift.id === shifts[x].id && emplo_schedus[z].employee.sector.id === sectors[y].id) {
                    //         var table = $('#table_reports_info tbody')
                    //         // var employeeTr = document.createElement("tr");
                    //         // var nameTd = document.createElement("td");
                    //         // var reasonTd = document.createElement("td")
                    //         // var extraHourTd = document.createElement("td")
                    //         //
                    //         // nameTd.textContent(emplo_schedus[z].employee.name)
                    //         // reasonTd.textContent(emplo_schedus[z].scheduling.reason)
                    //         // extraHourTd.textContent(emplo_schedus[z].employee.extra_hour)
                    //         //
                    //         // employeeTr.appendChild(nameTd)
                    //         // employeeTr.appendChild(reasonTd)
                    //         // employeeTr.appendChild(extraHourTd)
                    //         //
                    //         // var tableEmployee = document.querySelector('#table_funcionario_lider tbody');
                    //         //
                    //         // table.append("<tr>")
                    //         // table.append("<td>"+emplo_schedus[z].employee.name+"</td>")
                    //         // table.append("</tr>")
                    //         // console.log(emplo_schedus[z].employee.name)
                    //
                    //         table.append('<tr>\n' +
                    //             '                        <td>' + data['emplo_schedus_data'][z]['employee']['registration'] + '</td>\n' +
                    //             '                        <td>' + data['emplo_schedus_data'][z]['employee']['name'] + '</td>\n' +
                    //             '                        <td>' + data['emplo_schedus_data'][z]['scheduling']['reason'] + '</td>\n' +
                    //             '                        <td>' + data['emplo_schedus_data'][z]['employee']['extra_hour'] + '</td>\n' +
                    //             '                      </tr>')
                    //
                    //     }
                    //
                    // }

                    // }
                }
            }
        }
    })
})

function isPresent(all, element, comparation) {
    let result = all.find(ele => element === comparation)

    return result
}

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