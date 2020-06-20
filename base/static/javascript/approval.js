$("#form_director_list").submit(function (event) {
    event.preventDefault()
    var date = $('[name=date]').val()
    var shift = $('[name=shift]').val()
    var sector = $('[name=sector]').val()
    page = $('.director_list')
    $.ajax({
        url: 'diretor/lista',
        data: {'date': date, 'shift': shift, 'sector': sector},
        dateType: 'json',
        success: function (data) {
            const shifts = data.shifts
            const sectors = data.sectors
            const leaders = data.leaders
            const emplo_schedus = data.emplo_schedus
            console.log("teste")
            page.children().remove()
            page.append('<div class="row mt-4 mb-3">' +
                '<div class="col-3">' +
                '<img src="https://i.pinimg.com/originals/88/dd/e1/88dde1160aaebf6bfe42750b87afe11c.png" class="soonReport">' +
                '</div>' +
                '<div class="col-6">' +
                '<h1 class="text-center textTitleReport"><strong>RELATÓRIO DE HE | AG</strong></h1>' +
                '</div>' +
                '<div class="col-3">' +
                '</div>' +
                '</div>')
            // page.append('<form action="" method="post" id="approve_schedule">' )

            for (var x = 0; x < shifts.length; x++) {
                if (emplo_schedus.find(emplo_schedus => emplo_schedus.scheduling.shift.id === shifts[x].id)) {
                    page.append('<p class="text-left titleShiftsApro">Turno: <strong>' + shifts[x].name + '</strong></p>')
                }
                for (y = 0; y < sectors.length; y++) {
                    if (emplo_schedus.find(emplo_schedus => emplo_schedus.employee.sector.id === sectors[y].id && emplo_schedus.scheduling.shift.id === shifts[x].id)) {
                        page.append('<h1 class="text-center fontSetorGE"><strong>' + sectors[y].name + '</strong></h1>')
                    }
                    leaders_sector = leaders.filter(leaders => leaders.sector.id === sectors[y].id)
                    $.each(leaders_sector, function (key, value) {
                        if (emplo_schedus.find(emplo_schedus => emplo_schedus.employee.leader_name === value.name && emplo_schedus.scheduling.shift.id === shifts[x].id)) {
                            page.append('<h1 class="text-center text-muted mb-3 mt-5" style="font-size: 35px">' + value.name + '</h1>')
                            var tr = ""
                            var table = '<table class="table border border-dark fontTableGE" id="table_reports_info">\n' +
                                '  <thead class="theadAll mt-2">\n' +
                                '      <tr>\n' +
                                '          <th>Aprovado</th>\n' +
                                '          <th>Matricula</th>\n' +
                                '          <th>Funcionário</th>\n' +
                                '          <th>Função</th>\n' +
                                '          <th>Motivo</th>\n' +
                                '          <th>HE Previsto</th>\n' +
                                '       </tr>\n' +
                                '   </thead>\n' +
                                '<tbody class="mb-3">'
                            employees_leaders = emplo_schedus.filter(emplo_schedus => emplo_schedus.employee.leader_name === value.name)
                            $.each(employees_leaders, function (key, value) {
                                if (value.authorized === true) {
                                    checkbox = '<input id="check_approval" type="checkbox" value="' + value.employee.registration + '"  style="height: 25px; width: 25px" class="check_approval" checked>'
                                } else {
                                    checkbox = '<input id="check_approval" type="checkbox" value="' + value.employee.registration + '" style="height: 25px; width: 25px" class="check_approval">'
                                }
                                tr = tr + '<tr>\n' +
                                    '  <td>' + checkbox + '</td>\n' +
                                    '  <td style="padding-top: 17px">' + value.employee.registration + '</td>\n' +
                                    '  <td style="padding-top: 17px">' + value.employee.name + '</td>\n' +
                                    '  <td style="padding-top: 17px">' + value.employee.occupation + '</td>\n' +
                                    '  <td style="padding-top: 17px">' + value.scheduling.reason + '</td>\n' +
                                    '  <td style="padding-top: 17px">' + value.employee.extra_hour + '</td>\n' +
                                    '</tr>'
                            })
                            page.append(table + tr)
                            $(".check_approval").click(function () {
                                date = $("[name='date']").val()
                                alert(date)
                                registration = $(this).val()
                                if ($(this).prop("checked") === true) {
                                    situation = 'yes'
                                } else {
                                    situation = 'no'
                                }
                                // alert(situation + registration)
                                var csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
                                $.ajax({
                                    type: 'POST',
                                    url:'aprovacao',
                                    data: {'registration': registration, 'situation': situation,'csrfmiddlewaretoken': csrf,'date':date},
                                    dateType: 'json',
                                    success: function(data){  
                                        alert("Opa bom dia")
                                        console.log(data)
                                    }
                                })
                            })
                            // approve_schedule = '<div style="position:fixed ">'+
                            //                  '<input type="submit">'+
                            //                      '</div>'+
                            //                      '</form>'
                            // page.append(approve_schedule)

                        }
                    })
                }
            }

        }
    })
})
