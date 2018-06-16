'use strict';

$(document).ready(function () {

    var devicesTable;

    $('#devices-info').click();
    $.get(OPENHAB_API_ITEMS, function (res, status, req) {
        if (req.getResponseHeader('Content-Type') === 'application/json') {
            let data_display = [];
            for (let i = 0; i < res.length; i++) {
                data_display.push([
                    res[i].label,
                    res[i].type,
                    res[i].state,
                    //TODO: change group name of device
                    res[i].name
                ])
            }
            let columns = [
                {title: "Name"},
                {title: "Type"},
                {title: "State"},
                {title: "Group names"}
            ];
            if (devicesTable) {
                devicesTable.destroy();
            }
            devicesTable = create_datatables_info('pas-datatables-devices-info', data_display, columns);
        } else {
            alert('Cant not get device from OpenHAB!');
        }
    })
});