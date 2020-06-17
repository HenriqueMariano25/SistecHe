$(document).ready(function () {
    $(".leader").click(function () {
        registration = ($(this).val());
        if ($(this).prop("checked") === true) {
            situation = 'yes'
        } else {
            situation = 'no'
        }
        // alert(situation)
        $.ajax({
            url: 'lider',
            data: {
                'registration': registration,
                'situation': situation
            },
            dataType: 'json',
            success: function (data) {

            },
        });
    });

    // var allTrs = document.querySelectorAll('.tr-employee');
    // allTrs.forEach(function (tr) {

    //     tr.addEventListener("click", function () {
    //         var id_sector = tr.querySelector("#selected_sector").value;
    //         var csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    //         var employee_registration = tr.querySelector("#employee_registration").textContent;
    //         ajax_effective_sector(csrf, id_sector, employee_registration);
    //     });
    // });

    function ajax_effective_sector(csrf, id_sector, employee_registration) {
        $.ajax({
            type: 'POST',
            url: 'setor',
            data: {
                csrfmiddlewaretoken: csrf,
                action: 'post',
                id_sector: id_sector,
                employee_registration: employee_registration,
            },
            success: function (json) {
                console.log(json);
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    }
});