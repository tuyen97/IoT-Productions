'use strict';

$(document).ready(function () {

    let WARNING_API = '/pas/warning/';

    $('#warning_sidebar').click();

    let warning_table = $('#pas_datatables_warning').DataTable({
        "drawCallback": function (settings) {
            $('.btn_verify_member').on('click', function () {
                let user_id = $(this).data()['id'];
                let time_stamp = $(this).data()['time_stamp'];
                let tr = $(this).parents('tr');
                $.post(WARNING_API, {id: user_id, time_stamp: time_stamp})
                    .done(function (data) {
                        if (data.status === 'success') {
                            toastr.success(data.message, 'Success');
                            warning_table.row(tr).remove().draw();
                        }
                    })
                    .fail(function (err) {
                        console.log(err);
                        toastr.error("Have some error when delete this member!", "Fail");
                    })
            });

            $('.btn_discard_member').on('click', function () {
                let tr = $(this).parents('tr');
                toastr.remove();
                toastr.success('Discard log success!', 'Success');
                warning_table.row(tr).remove().draw();
            });
        }
    });

});

