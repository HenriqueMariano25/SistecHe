$("#select_leader_scheduling").change(function () {
    $("#tbody_funcionario_lider").children().remove();
    $("#tbody_he_estourada").children().remove();

    $('[name=seach_employee]').val("")

    $.ajax("agendamento/lider_selecionado?lider_id=" + this.value)

        .done(function (data) {
            var limite = data['limit_hour']['hours'];
            console.log(limite)
            for (var i = 0; i < data['employees'].length; i++) {
                var funcionarioTr = document.createElement("tr");
                var agendarTd = document.createElement("td");
                var matriculaTd = document.createElement("td");
                matriculaTd.setAttribute("class", "registration");
                var nomeTd = document.createElement("td");
                nomeTd.setAttribute("class", "name")
                var funcaoTd = document.createElement("td");
                funcaoTd.setAttribute("class", "occupation");
                var horaAcumuladaTd = document.createElement("td");
                horaAcumuladaTd.setAttribute("class", "accumuled_hour");

                var check_box = document.createElement("input");
                check_box.setAttribute("type", "checkbox");
                check_box.setAttribute("value", data['employees'][i]['registration']);
                check_box.setAttribute("name", "registrations");
                check_box.setAttribute("class", "check_employee checkS");
                // check_box.setAttribute("onclick", "teste()");

                agendarTd.appendChild(check_box);
                matriculaTd.textContent = data['employees'][i]['registration'];
                nomeTd.textContent = data['employees'][i]['name'];
                funcaoTd.textContent = data['employees'][i]['occupation'];
                horaAcumuladaTd.textContent = (parseFloat(data['employees'][i]['extra_hour']) + 7.30);

                if (data['employees'][i]['extra_hour'] >= (limite - 7.30)) {
                    var tabela_funcionario = document.querySelector('#table_he_estourada tbody');
                    // tabela_funcionario.setAttribute("onclick", "teste()");
                } else {
                    funcionarioTr.appendChild(agendarTd);
                    var tabela_funcionario = document.querySelector('#table_funcionario_lider tbody');
                    // tabela_funcionario.setAttribute("onclick", "teste()");
                }

                funcionarioTr.appendChild(matriculaTd);
                funcionarioTr.appendChild(nomeTd);
                funcionarioTr.appendChild(funcaoTd);
                funcionarioTr.appendChild(horaAcumuladaTd);

                tabela_funcionario.appendChild(funcionarioTr);
            }
            $("#leader_name").text(data['leader']['name']);
            $("#leader_occupation").text(data['leader']['occupation']);
        })
        .fail(function () {
            $("#nome_lider").text("");
            $("#funcao_lider").text("");
            $("#lider").val("0");
            $("#tbody_funcionario_lider").children().remove();
            $("#tbody_he_estourada").children().remove();

        });
});
$('#form_search_employee').submit(function (event) {
    event.preventDefault()
    $("#tbody_funcionario_lider").children().remove();
    $("#tbody_he_estourada").children().remove();
    search = $("[name=seach_employee]").val()
    var limite = $("#limite_hora").val();
    $.ajax({
        url: "buscar",
        data: {'search': search},
        dataType: 'json',
        success: function (data) {
            $("#select_leader_scheduling").val("0");
            if (data['employees'].length > 0) {
                add_employees_leader_table(data['leaders'], data['employees'], '#table_funcionario_lider tbody')
            }
            if (data['employees_burst'].length > 0) {
                add_employees_leader_table(data['leaders_burst'], data['employees_burst'], '#table_he_estourada tbody')
            }

        }
    })
})

function add_employees_leader_table(leaders, employees, table) {
    for (var x = 0; x < leaders.length; x++) {
        var leaderTr = document.createElement("tr")
        leaderTr.setAttribute("class", "leaderNotS")
        nameLeaderTd = document.createElement("td")
        nameLeaderTd.setAttribute("width", "100%")
        nameLeaderTd.setAttribute("colspan", 5)
        nameLeaderTd.setAttribute("style", "text-align: center;")
        nameLeaderTd.textContent = leaders[x]['name']
        const leader_table = document.querySelector(table);
        leaderTr.appendChild(nameLeaderTd);
        leader_table.appendChild(leaderTr);
        for (let i = 0; i < employees.length; i++) {
            if (employees[i]['leader_name'] === leaders[x]['name']) {
                const employeeTr = document.createElement("tr");
                const schedulingTd = document.createElement("td");
                const registrationTd = document.createElement("td");
                registrationTd.setAttribute("class", "registration pt-3");
                var nameTd = document.createElement("td");
                nameTd.setAttribute("class", "name pt-3")
                const occupationTd = document.createElement("td");
                occupationTd.setAttribute("class", "occupation pt-3");
                const accumuledHourTd = document.createElement("td");
                accumuledHourTd.setAttribute("class", "accumuled_hour pt-3 TESTE444");

                const check_box = document.createElement("input");
                check_box.setAttribute("type", "checkbox");
                check_box.setAttribute("value", employees[i]['registration']);
                check_box.setAttribute("name", "registrations");
                check_box.setAttribute("class", "check_employee checkS");

                schedulingTd.appendChild(check_box);
                registrationTd.textContent = employees[i]['registration'];
                nameTd.textContent = employees[i]['name'];
                occupationTd.textContent = employees[i]['occupation'];
                accumuledHourTd.textContent = (parseFloat(employees[i]['extra_hour']) + 7.30);

                var employee_table = document.querySelector(table);

                if (table == '#table_funcionario_lider tbody') {
                    employeeTr.appendChild(schedulingTd);
                }

                employeeTr.appendChild(registrationTd);
                employeeTr.appendChild(nameTd);
                employeeTr.appendChild(occupationTd);
                employeeTr.appendChild(accumuledHourTd);

                employee_table.appendChild(employeeTr);
            }
        }
    }
}

$('#form_scheduling_employees').submit(function (event) {
    event.preventDefault()
    // const registrations = $('[name=registrations]:checked').val()
    let registrations = $("input:checkbox[name=registrations]:checked").map(function () {
        return $(this).val()
    }).get()
    let date = $('[name=scheduling_date]').val()
    let leader = $('[name=leader]').val()
    let shift = $('[name=shift]').val()
    let reason = $('[name=reason]').val()
    let csrf = $('[name=csrfmiddlewaretoken]').val()
    $.ajax({
        url: 'funcionario/agendar',
        method: 'post',
        data: {
            'scheduling_date': date,
            'reason': reason,
            'registrations': registrations,
            'shift': shift,
            'leader': leader,
            'csrfmiddlewaretoken': csrf,
        },
        dataType: 'json',
        success: function (data) {
            if (typeof data.scheduled_employees !== "undefined") {
                let div_alerts = $('#alerts_scheduling')
                div_alerts.children().remove();
                let scheduled_employees = data.scheduled_employees
                console.log(scheduled_employees)
                div_alerts.append('<div class="alert alert-danger"><h3 class="alert-heading"><strong>Os Funcionários Abaixo Já Foram Agendados</strong></h3></div>')
                $.each(scheduled_employees, function (key, value) {
                    console.log(value)
                    div_alerts.append('<div class="alert alert-danger">' +
                        ' <p class="textAlertS">' + value.employee.registration + '  -  ' + value.employee.name + '</p>' +
                        ' </div>')
                })

            } else {
                let div_alerts = $('#alerts_scheduling')
                div_alerts.children().remove();
                div_alerts.append('<div class="alert alert-success text-center"><h3><strong>Agendamento Realiza com Sucesso</strong></h3></div>')
                $("#tbody_funcionario_lider").children().remove();
                $("#tbody_he_estourada").children().remove();
                $('[name=leader]').val(0)
            }
        }
    })
})

$("#select_all").click(function () {
    $('input:checkbox').not(this).prop('checked', this.checked);
});

$("#edit_scheduling").submit(function (event) {
    event.preventDefault()
    let date = $('#date').val()
    let csrf = $('[name=csrfmiddlewaretoken]').val()
    $.ajax({
        url: 'editar/lista',
        method: "POST",
        dataType: 'json',
        data: {
            'csrfmiddlewaretoken': csrf,
            'date': date,
        },
        success: function (data) {
            const emplo_schedus = data.emplo_schedus
            page = $('#list_edit_employees_')
            let table = '<table class="table fontTableGE" id="table_reports_info">\n' +
                '  <thead class="theadAll">\n' +
                '      <tr>\n' +
                '          <th>Matricula</th>\n' +
                '          <th>Funcionário</th>\n' +
                '          <th>Função</th>\n' +
                '          <th>Motivo</th>\n' +
                '          <th>HE Previsto</th>\n' +
                '          <th>Deletar</th>\n' +
                '       </tr>\n' +
                '   </thead>\n' +
                '<tbody>'
            $.each(emplo_schedus, function (key, value) {
                let tr = '<tr>\n' +
                    '  <td style="padding-top: 17px" id="employee_registration">' + value.employee.registration + '</td>\n' +
                    '  <td style="padding-top: 17px">' + value.employee.name + '</td>\n' +
                    '  <td style="padding-top: 17px">' + value.employee.occupation + '</td>\n' +
                    '  <td style="padding-top: 17px">' + value.scheduling.reason + '</td>\n' +
                    '  <td style="padding-top: 17px">' + value.employee.extra_hour + '</td>\n' +
                    '  <td><button class="delete_employees btn btn-danger btn-block">Deletar</button></td>\n' +
                    '</tr>'
                table = table + tr
            })
            page.append(table)
            $(".delete_employees").click(function () {
                const result = confirm("Deseja mesmo excluir essa marcação ?")
                if (result === true) {
                    let row = ($(this).parent().parent())
                    let registration = row.find("#employee_registration").text()
                    $.ajax({
                        method: "POST",
                        url: "deletar",
                        data: {
                            'date': date,
                            'csrfmiddlewaretoken': csrf,
                            'registration': registration,
                        },
                        dataType: "json",
                        success: function (data) {
                            if (data.status === "success") {
                                row.remove();
                            }
                        }
                    })
                }
            });
        }
    })
})