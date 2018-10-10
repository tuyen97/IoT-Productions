'use strict';

let OPENHAB_API_ITEMS = "http://localhost:8080/rest/items";

let MQTT_CONNECT_TIMEOUT = 5000;
let MQTT_HOSTNAME = "localhost";
let MQTT_PORT = 9001;
// let MQTT_PATH = "/mqtt";
let MQTT_TOPIC_USER_REGISTER = "pas/mqtt/rfid/user_register";
let MQTT_TOPIC_LATEST_USER_SCAN = "pas/mqtt/server/latest_scan";
let MQTT_TOPIC_USER_CHANGE = "pas/mqtt/rfid/user_change";
let MQTT_TOPIC_RFID_ACTION = "pas/mqtt/rfid/action";
let MQTT_MEMBER_DOES_NOT_EXIST="pas/mqtt/member/does_not_exist";

$('.pas-sidebar-element').each(function (index) {
    $(this).on('click', function () {
        if (!$(this).hasClass('active')) {
            $('ul.sidebar-menu li.pas-sidebar-element.active').removeClass('active');
            $(this).addClass('active');
        }
    })
});

let create_datatables_info = function (selector, data, columns) {
    return $('#' + selector).DataTable({
        data: data,
        columns: columns
    });
};


window.setTimeout(function() {
  $(".alert").fadeTo(500, 0).slideUp(500, function(){
      $(this).remove();
  });
}, 5000);
