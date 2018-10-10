'use strict';

$(document).ready(function () {
    $('#dashboard').click();

    $('#today_timeline').html(moment().format('L'));

    $.ajax({
        type: "get",
        url: '/pas/warning',
        data: {is_get_all: true},
        success: function (data, text) {
            if (data.status === 'success') {
                $('#box_warning_value').html(data.data);
            } else {
                toastr.error('Cannot get number of warning!', 'Fail');
            }
        },
        error: function (request, status, error) {
            console.log(error);
            toastr.error('Cannot get number of warning!', 'Fail');
        }
    });

    let client;

    // MQTT client
    let options = {
        clientId: 'pas_' + Math.random().toString().split('.')[1],
        connectTimeout: MQTT_CONNECT_TIMEOUT,
        hostname: MQTT_HOSTNAME,
        port: MQTT_PORT,
    };

    client = mqtt.connect(options);

    client.on('connect', function () {
        client.subscribe(MQTT_TOPIC_LATEST_USER_SCAN);
        client.subscribe(MQTT_MEMBER_DOES_NOT_EXIST);
    });

    client.on('message', function (topic, message) {
        console.log(topic);
        if(topic == MQTT_TOPIC_LATEST_USER_SCAN){
            message = JSON.parse(message);
            toastr.warning("<strong>" + message.member_name + "</strong> is <strong>" + message.state +
                    "</strong><br/> Please reload to see!")
        }else{
            toastr.warning("Can't recognize this card id");
        }
    });

});

