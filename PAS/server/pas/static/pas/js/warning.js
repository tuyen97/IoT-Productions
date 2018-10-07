'use strict';

$(document).ready(function () {

    let WARNING_API = '/pas/warning/';

    $('#warning_sidebar').click();
    $('.btn_verify_member').on('click', function () {
        let user_id = $(this).data()['id'];
        let time_stamp = $(this).attr('data-time_stamp');
        console.log(time_stamp);
        let tr = $(this).closest('tr');
        $.post(WARNING_API, {id: user_id, time_stamp: time_stamp})
            .done(function (data) {
                if (data.status === 'success') {
                    toastr.success(data.message, 'Success');
                    tr.remove();
                }
            })
            .fail(function (err) {
                console.log(err);
                toastr.error("Have some error when delete this member!", "Fail");
            })
    });

    $('.btn_discard_member').on('click', function () {
        let user_id = $(this).data()['id'];
        let time_stamp = $(this).attr('data-time_stamp');
        console.log(time_stamp);
        let tr = $(this).closest('tr');
        $.post(WARNING_API, {id: user_id, time_stamp: time_stamp})
            .done(function (data) {
                if (data.status === 'success') {
                    toastr.success(data.message, 'Success');
                    tr.remove();
                }
            })
            .fail(function (err) {
                console.log(err);
                toastr.error("Have some error when delete this member!", "Fail");
            })
    });
});

