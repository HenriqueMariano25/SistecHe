$("#select_leader_scheduling").change(function () {
    $("#tbody_funcionario_lider").children().remove();
    $("#tbody_he_estourada").children().remove();

    $('[name=seach_employee]').val("")
    var limite = $("#limite_hora").val();
    $.ajax("agendamento/lider_selecionado?lider_id=" + this.value)
        .done(function (data) {
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
                check_box.setAttribute("class", "check_employee");
                // check_box.setAttribute("onclick", "teste()");

                agendarTd.appendChild(check_box);
                matriculaTd.textContent = data['employees'][i]['registration'];
                nomeTd.textContent = data['employees'][i]['name'];
                funcaoTd.textContent = data['employees'][i]['occupation'];
                horaAcumuladaTd.textContent = (parseFloat(data['employees'][i]['extra_hour']) + 7.30);

                if (data['employees'][i]['extra_hour'] >= limite - 7.30) {
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
$('#submit_search_employee').click(function () {
    $("#tbody_funcionario_lider").children().remove();
    $("#tbody_he_estourada").children().remove();
    search = $("[name=seach_employee]").val()
    var limite = $("#limite_hora").val();
    console.log(search)
    $.ajax({
        url: "buscar",
        data: {'search': search},
        dataType: 'json',
        success: function (data) {
            $("#select_leader_scheduling").val("0");
            console.log(data);
            console.log("oi");
            console.log(data['employees'].length)
            if(data['employees'].length > 0){
                add_employees_leader_table(data['leaders'],data['employees'],'#table_funcionario_lider tbody')
            }
            if(data['employees_burst'].length > 0){
                add_employees_leader_table(data['leaders_burst'],data['employees_burst'],'#table_he_estourada tbody')
            }

        }
    })
})

function add_employees_leader_table(leaders, employees,table) {
    for (var x = 0; x < leaders.length; x++) {
        var leaderTr = document.createElement("tr")
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
                registrationTd.setAttribute("class", "registration");
                var nameTd = document.createElement("td");
                nameTd.setAttribute("class", "name")
                const occupationTd = document.createElement("td");
                occupationTd.setAttribute("class", "occupation");
                const accumuledHourTd = document.createElement("td");
                accumuledHourTd.setAttribute("class", "accumuled_hour");

                const check_box = document.createElement("input");
                check_box.setAttribute("type", "checkbox");
                check_box.setAttribute("value", employees[i]['registration']);
                check_box.setAttribute("name", "registrations");
                check_box.setAttribute("class", "check_employee");

                schedulingTd.appendChild(check_box);
                registrationTd.textContent = employees[i]['registration'];
                nameTd.textContent = employees[i]['name'];
                occupationTd.textContent = employees[i]['occupation'];
                accumuledHourTd.textContent = (parseFloat(employees[i]['extra_hour']) + 7.30);

                var employee_table = document.querySelector(table);

                if(table == '#table_funcionario_lider tbody'){
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


// $("#scheduling_employees").on("ajax:success", function (event) {
//     console.log(event.detail);
//     lider = $("#lider option:selected").val();
//     if (lider != 0) {
//         teste = $('texto_msg_erro');
//         msg_erro = event.detail[0].erro
//         if (msg_erro != undefined) {
//             alert(msg_erro);
//         } else {
//             $("#tbody_funcionario_lider").children().remove();
//             $("#tbody_he_estourada").children().remove();
//             $("#agendar_data").val("0");
//             $("#agendar_turno").val("");
//             $("#agendar_motivo").val("");
//             $("#nome_lider").text("");
//             $("#funcao_lider").text("");
//             $("#select_lider_marcacao").val("0");
//             $(".msg-erro p").text("Agendamento realizado com sucesso");
//             $(".msg-erro").show();
//             $("body").mouseup(function () {
//                 $(".msg-erro").hide();
//             });
//         }
//     } else {
//         alert("Favor selecione um lider");
//     }
// });