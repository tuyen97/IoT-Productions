'use strict';

let TRAIN_URL = '/pas/member/train/';
let MEMBER_API = '/pas/api/member/';
let CHANGE_CARD_ID_API = '/pas/api/change-card-id/';
let VIDEO_TIME = 15;

$(document).ready(function () {
    $('#members-info').click();

    // moment.locale('vi');

    let member_uuid = $('#btn_change_avatar').data()['id'];

    change_rfid_card();

    $('#start_get_video_train').on('click', function () {

        let self = this;

        // capture camera and/or microphone
        navigator.mediaDevices.getUserMedia({
            video: true,
            audio: true
        }).then(function (camera) {
            let video_train_element = $('#your-video-id')[0];

            // preview camera during recording
            video_train_element.muted = true;
            video_train_element.srcObject = camera;

            // recording configuration/hints/parameters
            let recordingHints = {
                type: 'video',
                disableLogs: true
            };

            // initiating the recorder
            let recorder = RecordRTC(camera, recordingHints);

            // starting recording here
            recorder.startRecording();

            // auto stop recording after 5 seconds
            let milliSeconds = VIDEO_TIME * 1000;
            setTimeout(function () {

                // stop recording
                recorder.stopRecording(function () {
                    // get recorded blob
                    let blob = recorder.getBlob();

                    let id = $(self).data()['id'];
                    let fileName = $(self).data()['name'] + ".webm";
                    let fileObject = new File([blob], fileName, {
                        type: 'video/webm'
                    });

                    let formData = new FormData();

                    formData.append('id', id);

                    // recorded data
                    formData.append('video-train', fileObject);

                    // file name
                    formData.append('video-filename', fileObject.name);

                    console.log("Video size upload: " + bytesToSize(fileObject.size));

                    // upload using jQuery
                    $.ajax({
                        url: '/api/upload_video/', // replace with your own server URL
                        data: formData,
                        cache: false,
                        contentType: false,
                        processData: false,
                        type: 'POST',
                        success: function (response) {
                            console.log('out put of post video');
                            console.log(response);
                            if (response.status === 'success') {
                                $('#start_get_video_train').attr('disabled', 'disabled');
                                toastr.success(response.message, 'Success');
                            } else if (response.status === 'warning') {
                                toastr.warning(response.message, 'Warning');
                            }
                        }
                    });

                    // open recorded blob in a new window
                    window.open(URL.createObjectURL(blob));

                    // release camera
                    video_train_element.srcObject = null;
                    camera.getTracks().forEach(function (track) {
                        track.stop();
                    });

                    // you can preview recorded data on this page as well
                    video_train_element.src = URL.createObjectURL(blob);

                });

            }, milliSeconds);
        });
    });


    let btn_train = $('#btn_train');

    btn_train.on('click', function () {
        btn_train.button('loading');
        let member_id = $(this).data()['id'];
        let self = this;
        $.ajax({
            type: "get",
            url: TRAIN_URL,
            data: {id: member_id, isTrain: true},
            success: function (data, text) {
                if (data.status === 'success') {
                    toastr.success(data.message, 'Success');
                    $(self).button('disable');
                    // btn_train.button('reset').attr('disabled', 'disabled');
                    $('#btn_train').button('reset');
                    $('#member_train_warning').html('Done!').css('color', 'green');
                    $('#member_threshold').html(data.threshold);
                    $('#btn_train').attr('disabled', 'disabled');
                } else if (data.status === 'warning') {
                    toastr.warning(data.message, 'Warning');
                    $(self).button('reset').attr('disabled', 'disabled');
                } else {
                    toastr.error('Cannot train!', 'Fail');
                    $(self).button('reset').removeAttr('disabled');
                }
            },
            error: function (request, status, error) {
                console.log(error);
                toastr.error(error, 'Fail');
                $(self).button('reset').removeAttr('disabled');
            }
        });
    });

    $('#btn_get_more_calculate_money').on('click', function () {
        let member_id = $(this).data()['id'];
        $.ajax({
            type: "get",
            url: '/pas/calculate_hour/',
            data: {id: member_id},
            success: function (data, text) {
                if (data.status === 'success') {
                    toastr.success(data.message, 'Success');
                    console.log(data);
                }
            },
            error: function (request, status, error) {
                console.log(error);
            }
        });
    });

    $('#btn_change_avatar').on('click', function () {
        $(this).css('display', 'none');
        $('.change_avatar_container').css('display', '');
    });

    $('#upload_avatar').change(function (e) {
        let self = $(this);

        let img_url = URL.createObjectURL(e.target.files[0]);
        $('#img_member_avatar').attr('src', img_url);
        let img = e.target.files[0];
        let data = new FormData();
        data.append('type', 'upload_avatar');
        data.append('id', self.data()['id']);
        data.append('img', img);

        console.log(img);
        $.ajax({
            type: "post",
            contentType: false,
            processData: false,
            url: MEMBER_API,
            data: data,
            success: function (data, text) {
                $('.change_avatar_container').css('display', 'none');
                $('#btn_change_avatar').css('display', '');
                toastr.success(data.message, 'Success');
            },
            error: function (request, status, error) {
                console.log(error);
            }
        });
    });

    $('#btn_cancel_change_avatar').on('click', function () {
        $('.change_avatar_container').css('display', 'none');
        $('#btn_change_avatar').css('display', '');
    });

    function change_rfid_card() {
        let btn_change_card_el = $('#btn-change-card');
        let btn_save_card_el = $('#btn-save-change-card');
        let btn_cancel_card_el = $('#btn-cancel-change-card');
        let old_card_id = $('#card-id').text();
        let new_card_id;

        btn_change_card_el.on('click', function () {
            // MQTT client
            let options = {
                clientId: 'pas_change_card_' + Math.random().toString().split('.')[1],
                connectTimeout: MQTT_CONNECT_TIMEOUT,
                hostname: MQTT_HOSTNAME,
                port: MQTT_PORT,
            };

            let client = mqtt.connect(options);

            client.on('connect', function () {
                client.subscribe(MQTT_TOPIC_USER_CHANGE);
                client.publish(MQTT_TOPIC_RFID_ACTION, '{"action":"change_topic"}')
                btn_change_card_el.button('loading');
            });

            client.on('message', function (topic, message) {
                new_card_id = message.toString();
                $('#card-id').html(new_card_id);
                btn_save_card_el.css('display', '');
                btn_cancel_card_el.css('display', '');
                btn_change_card_el.css('display', 'none').button('reset');
                // $('#id_card_id_temp').css('display', '').html(message.toString());
                // $('#btn-scan-rfid').removeAttr('disabled').html('Re-scan');
                // $('#btn_submit_new_member').removeAttr('disabled');
                client.end();
            });
        });

        btn_cancel_card_el.on('click', function () {
            $('#card-id').html(old_card_id);
            btn_save_card_el.css('display', 'none');
            btn_cancel_card_el.css('display', 'none');
            btn_change_card_el.css('display', '');
        });

        btn_save_card_el.on('click', function () {
            if (new_card_id) {
                $.ajax({
                    type: "post",
                    url: CHANGE_CARD_ID_API,
                    data: {
                        new_card_id: new_card_id,
                        old_card_id: old_card_id
                    },
                    success: function (data, text) {
                        btn_save_card_el.css('display', 'none');
                        btn_cancel_card_el.css('display', 'none');
                        btn_change_card_el.css('display', '');
                        toastr.success(data.message, 'Success');
                    },
                    error: function (request, status, error) {
                        console.log(error);
                    }
                });
            } else {
                alert('Can not read new card id');
            }
        });
    }

    function get_salary(member_uuid) {

        let d = new Date();
        let today_unix = parseInt(Math.round((d).getTime() / 1000));
        let seven_days_ago = d.setDate(d.getDate() - 7);
        seven_days_ago = parseInt(seven_days_ago / 1000);

        $.ajax({
            type: "get",
            url: 'http://192.168.60.82:9090/get_salary_in_period',
            data: {
                id: member_uuid.toString(),
                started_date: seven_days_ago.toString(),
                ended_date: today_unix.toString()
            },
            // crossDomain: true,
            headers: {
                'Access-Control-Allow-Origin': '*'
            },
            success: function (data, text) {
                console.log(data);
                if (data.status === 'SUCCESS') {
                    let salaries = data.result;
                    let rows = '';
                    for (let i = 0; i < salaries.length; i++) {
                        let day = moment.unix(salaries[i].unix_time).format('DD/MM/YYYY');
                        rows += ' <tr>' +
                            '<td>' + day + '</td>' +
                            '<td>' + salaries[i].work_time + '</td>' +
                            '<td>' + salaries[i].day_salary + '</td>' +
                            '<td><i class="fa fa-star text-warning"></i>' +
                            '<i class="fa fa-star text-warning"></i>' +
                            '<i class="fa fa-star text-warning"></i>' +
                            '<i class="fa fa-star text-warning"></i>' +
                            '<i class="fa fa-star-half-full text-warning"></i>' +
                            '</td>' +
                            '</tr>';
                    }
                    $('#table_time_line tr:last').after(rows);
                }
            },
            error: function (request, status, error) {
                console.log(error);
            }
        });
    }

});