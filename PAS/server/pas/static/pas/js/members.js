'use strict';

let MEMBERS_INFO_API = '/pas/api/members';
let MEMBERS_API = '/pas/members-info/';

$(document).ready(function () {

    let card_id_element = $('#id_card_id');
    card_id_element.removeAttr('required').parent().css('display', 'none');
    if(card_id_element.val()){
        $('#id_card_id_temp').html(card_id_element.val()).css('display','');
    }
    $('#id_position').select2({
        width: '100%'
    });

    $('#members-info').click();
    let user_id;
    let tr_clicking;
    let table_members = $('#pas_datatables_members_info').DataTable({
        "dom": 'lf<"#btn_add_member_container">rtip',
        "drawCallback": function (settings) {
            $('.btn_delete_member').on('click', function () {
                user_id = $(this).data()['id'];
                tr_clicking = $(this).parents('tr');
                console.log(user_id);
            });
        }
    });
    $('#btn_add_member_container').css("float", "right");
    $('#btn_add_member').appendTo('#btn_add_member_container')
        .css({marginRight: "10px", marginBottom: "15px"});

    // $.get(MEMBERS_INFO_API, function (res, status, req) {
    //     console.log(res);
    // });

    $('#btn-scan-rfid').on('click', scan_rfid_card);
    submit_new_member_event();
    $('#btn_submit_delete_member').on('click', function () {
        console.log(user_id);
        $.post(MEMBERS_API, {id: user_id, action: 'delete'})
            .done(function (data) {
                if (data.status === 'success') {
                    toastr.success(data.message, 'Success');
                    table_members.row(tr_clicking).remove().draw();
                }
                else if (data.status === 'fail') {
                    toastr.error(data.message, 'Fail');
                }
                $('#modal-delete-user').modal('toggle');
            })
            .fail(function (err) {
                console.log(err);
                $('#modal-delete-user').modal('toggle');
                toastr.error("Have some error when delete this member!", "Fail");
            })
    });
});

function scan_rfid_card() {

    $('#id_card_id_container').find('div p i').css('display', '');
    $('#id_card_id_temp').css('display', 'none');
    $(this).attr('disabled', 'disabled');
    $('#btn_submit_new_member').attr('disabled', 'disabled');

    // MQTT client
    let options = {
        clientId: 'pas',
        connectTimeout: MQTT_CONNECT_TIMEOUT,
        hostname: MQTT_HOSTNAME,
        port: MQTT_PORT,
    };

    let client = mqtt.connect(options);

    client.on('connect', function () {
        client.subscribe(MQTT_TOPIC_USER_REGISTER);
    });

    client.on('message', function (topic, message) {
        $('#id_card_id_container').find('div p i').css('display', 'none');
        $('#id_card_id_temp').css('display', '').html(message.toString());
        $('#btn-scan-rfid').removeAttr('disabled').html('Re-scan');
        $('#btn_submit_new_member').removeAttr('disabled');
        client.end();
    });
}

function submit_new_member_event() {
    $("#new_member_form").submit(function (event) {

        let card_id = $('#id_card_id_temp').text();
        if (card_id) {
            console.log(card_id);
            $('#id_card_id').val(card_id);
        } else {
            alert('Miss card ID!');
            event.preventDefault();
        }
    }).bind('ajax:complete', function () {
        alert('add user success!');
    });
}

