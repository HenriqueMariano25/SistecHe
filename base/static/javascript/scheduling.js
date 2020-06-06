// $(document).ready(function () {
//     $(".check_employee").click(function () {
//         registration = ($(this).val());
//         alert("oi");
//     });
// });



$("#select_leader_scheduling").change(function () {
    $("#tbody_funcionario_lider").children().remove();
    $("#tbody_he_estourada").children().remove();
    var limite = $("#limite_hora").val();
    $.ajax("agendamento/lider_selecionado?lider_id=" + this.value)
        .done(function (data) {
            for (var i = 0; i < data['employees'].length; i++) {
                var funcionarioTr = document.createElement("tr");
                var agendarTd = document.createElement("td");
                var matriculaTd = document.createElement("td");
                var nomeTd = document.createElement("td");
                var funcaoTd = document.createElement("td");
                var horaAcumuladaTd = document.createElement("td");

                var check_box = document.createElement("input");
                check_box.setAttribute("type", "checkbox");
                check_box.setAttribute("value", data['employees'][i]['registration']);
                check_box.setAttribute("name", "registrations");
                check_box.setAttribute("class", "check_employee");
                check_box.setAttribute("onclick", "teste()");

                agendarTd.appendChild(check_box);
                matriculaTd.textContent = data['employees'][i]['registration'];
                nomeTd.textContent = data['employees'][i]['name'];
                funcaoTd.textContent = data['employees'][i]['occupation'];
                horaAcumuladaTd.textContent = (parseFloat(data['employees'][i]['extra_hour']) + 7.30);

                if (data['employees'][i]['extra_hour'] >= limite - 7.30) {
                    var tabela_funcionario = document.querySelector('#table_he_estourada tbody');
                } else {
                    funcionarioTr.appendChild(agendarTd);
                    var tabela_funcionario = document.querySelector('#table_funcionario_lider tbody');
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



$("#scheduling_employees").on("ajax:success", function (event) {
    console.log(event.detail);
    lider = $("#lider option:selected").val();
    if (lider != 0) {
        teste = $('texto_msg_erro');
        msg_erro = event.detail[0].erro
        if (msg_erro != undefined) {
            alert(msg_erro);
        } else {
            $("#tbody_funcionario_lider").children().remove();
            $("#tbody_he_estourada").children().remove();
            $("#agendar_data").val("0");
            $("#agendar_turno").val("");
            $("#agendar_motivo").val("");
            $("#nome_lider").text("");
            $("#funcao_lider").text("");
            $("#select_lider_marcacao").val("0");
            $(".msg-erro p").text("Agendamento realizado com sucesso");
            $(".msg-erro").show();
            $("body").mouseup(function () {
                $(".msg-erro").hide();
            });
        }
    } else {
        alert("Favor selecione um lider");
    }
});

function teste(){
    console.log($(this).parent());
}