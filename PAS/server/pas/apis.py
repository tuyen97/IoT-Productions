import datetime, time
import requests
from django.http import Http404, HttpResponse, JsonResponse
from django.utils.timezone import now, localtime
from django.contrib.auth.decorators import login_required

from .models import Member, Logs, Money
from . import const


def test(request):

    return JsonResponse({'ok': 'ok'})


@login_required()
def calculate_hour(request):
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    members = Member.objects.all()
    data_send_to_BC = []
    for member in members:
        if member.email != 'admin@icse.com':
            logs_for_today = Logs.objects.filter(time_stamp__range=(today_min, today_max),
                                                 member_id=member.id)
            total_hour = None
            if len(logs_for_today):
                for log in logs_for_today:
                    if log.is_go_in:
                        start_time = log.time_stamp
                    else:
                        # check start_time
                        if total_hour:
                            total_hour += log.time_stamp - start_time
                        else:
                            total_hour = log.time_stamp - start_time
                        start_time = None
                if total_hour:

                    hour_convert = divmod(total_hour.days * 86400 + total_hour.seconds, 60)

                    local_today = localtime(now()).date()
                    money = Money(member=member,total_hour=hour_convert[0],date=local_today)
                    money.save()

            #         TODO: Remove commend to enable request to Blockchain
            # today_unix_time = time.time()
            # # today_unix_time = time.mktime(datetime.date.today().timetuple())
            # today_unix_time = int(today_unix_time)
            # hour_convert = 8
            # data_send_to_BC.append(
            #     {'id': str(member.id), 'work_time': str(hour_convert), 'unix_time': str(today_unix_time)}
            # )
    # if data_send_to_BC:
    #     data = {
    #         'data': data_send_to_BC
    #     }
    #     calculate_salary_url = const.BC_SERVER + const.BC_API_CALCULATE_SALARY_USER
    #     r = requests.post(calculate_salary_url, json=data)
    #     result = r.json()

    return JsonResponse({'ok': 'ok'})


def server_api(request):
    # server_uuid = request.GET['uuid']
    http_response = {
        'servername': 'dongdz',
        'uuid': 'edb7ea39-310d-4b07-a750-758c944cc940',
        'ip': '192.168.1.1',
        'hostname': 'beo-cute'
    }
    return JsonResponse(http_response)

