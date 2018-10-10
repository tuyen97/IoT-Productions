import os, uuid, datetime, pytz, shutil
import json
import requests
from django.utils import timezone, dateparse
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.files.images import ImageFile, File
from django.core.files.storage import default_storage
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login

from .security.pas_authentication_backend import PasBackend

from .member_forms import AddMemberForm
from .models import Member, Logs, Money
from .security.login_form import LoginForm

from . import get_faces_to_train, face_train, face_recognize, const, \
    mqtt, face_detection

from server import settings

mqtt.client.loop_start()
@login_required()
def index(request):
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    logs_for_today = Logs.objects.filter(time_stamp__range=(today_min, today_max))
    member_have_log_today = []
    for log in logs_for_today:
        if(log.member not in member_have_log_today):
            member_have_log_today.append(log.member)
    members_in_lab = Member.objects.filter(is_in_lab=True)
    member_in_lab_now=[]
    for member in members_in_lab:
        print(member.name)
        if(member in member_have_log_today):
            member_in_lab_now.append(member)

    context = {
        'logs': logs_for_today,
        'members_in_lab': member_in_lab_now
    }
    return render(request, 'pas/index.html', context)


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('/pas/login')


def login_view(request):
    logout(request)
    if request.method == 'GET':
        context = {
            'form': LoginForm
        }
        return render(request, 'pas/login.html', context)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = PasBackend().authenticate(email=email, password=password)
        if user is not None:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('/pas')
            # return render(request, 'pas/404_error.html')
        else:
            http_response = {
                'status': 'fail',
                'message': 'Email or password not correct!',
            }
            return JsonResponse(http_response)


@login_required()
def devices_info(request):
    return render(request, 'pas/404_error.html')


@login_required()
def warning(request):
    if request.method == 'POST':
        id = request.POST['id']
        uid = uuid.UUID(id).hex
        # request.POST['time_stamp'] = "2018-04-17 23:04:34"
        time_stamp = dateparse.parse_datetime(request.POST['time_stamp'])
        #time_stamp=request.POST['time_stamp']
  #      tz = pytz.timezone(settings.TIME_ZONE).localize(time_stamp)
        print("ok")
       # log1 = Logs.objects.filter(time_stamp=time_stamp)
        log = Logs.objects.filter(member_id=uid, time_stamp=time_stamp).first()

        # log.image.delete(save=True)
        #log = Logs.objects.all()
        #l=log.first()
        log.result_auth = True
        log.save()

        http_response = {
            'status': 'success',
            'message': 'Verify member success!',
        }
        return JsonResponse(http_response)
    logs_warning = Logs.objects.filter(result_auth=False).all()

    # api to get number of warning to display on side bar
    if 'is_get_all' in request.GET:
        http_response = {
            'status': 'success',
            'data': len(logs_warning),
        }
        return JsonResponse(http_response)
    context = {
        'logs_warning': logs_warning
    }
    return render(request, 'pas/warning.html', context)


@login_required()
def members_info(request):
    form = AddMemberForm
    if request.method == 'POST':
        post_data = request.POST
        # edit or delete member
        if 'id' in post_data:
            if post_data['action'] == 'delete':
                member_id = post_data['id']
                member = Member.objects.get(id=member_id)
                if member.email == 'admin@icse.com':
                    http_response = {
                        'status': 'fail',
                        'message': "Can't delete admin!",
                    }
                    return JsonResponse(http_response)

                logs = Logs.objects.filter(member_id=member_id)
                if len(logs):
                    for log in logs:
                        log.image.delete(save=True)
                        log.delete()
                # member.avatar.delete(save=True)

                label = member.recognize_label
                # delete train and test images
                faces_train_path = os.path.join(const.FACE_TRAIN_FOLDER, str(label))
                if os.path.isdir(faces_train_path):
                    shutil.rmtree(faces_train_path)

                # delete file model .yml
                eigenface_model_path = os.path.join(const.EIGENFACES_FOLDER, str(label) + ".yml")
                if os.path.isfile(eigenface_model_path):
                    os.remove(eigenface_model_path)

                member.delete()
                # TODO: un-comment for send request to Blockchain server
                # del_url = const.BC_SERVER + const.BC_API_DEL_USER
                # data = {
                #     'id': str(member.id)
                # }
                # r = requests.post(del_url, json=data)
                # result = r.json()
                http_response = {
                    'status': 'success',
                    'message': 'Delete member success on PAS !',
                }
                # if result['status'] == 'SUCCESS':
                #     http_response['message'] = 'Delete member success on PAS and Blockchain server'
                # else:
                #     messages.error(request, result['message'])
                return JsonResponse(http_response)
            elif post_data['action'] == 'edit':
                pass
        # add member
        else:
            # create a form instance and populate it with data from the request:
            form = AddMemberForm(request.POST)
            member_uuid = uuid.uuid4()
            # check whether it's valid:
            if form.is_valid():
                u = Member(
                    id=member_uuid,
                    name=form.data['name'],
                    email=form.data['email'],
                    card_id=form.data['card_id'],
                    course=form.data['course'],
                    research_about=form.data['research_about'],
                    coefficient=form.data['coefficient'],
                    position=form.data['position']
                )
                u.save()

                # TODO: un-comment for send request to Blockchain server
                # url = const.BC_SERVER + const.BC_API_ADD_USER
                # data = {
                #     'id': str(member_uuid),
                #     'rfid': form.data['card_id'],
                #     'username': form.data['name']
                # }
                # r = requests.post(url, json=data)
                #
                # result = r.json()
                # if result['status'] == 'SUCCESS':
                #     u.is_added_to_blockchain = True
                #     u.save()
                # else:
                #     messages.error(request, result['message'])

                messages.success(request, 'Add member success to PAS!')
                return redirect(request.path)
            else:
                messages.error(request, 'Add user fail. See detail in form!')

    try:
        member_list = Member.objects.all()
        context = {
            'member_list': member_list,
            'form': form,
        }
    except Member.DoesNotExist:
        raise Http404("Member table does not exist")
    return render(request, 'pas/member/index.html', context)


@login_required()
def member_api(request):
    if request.method == 'POST':
        if 'type' in request.POST:
            id = request.POST['id']
            member = Member.objects.get(id=id)
            file = request.FILES['img']
            image_end_code = file.name.split('.')[1]
            avatar_name = member.name.replace(' ', '_') + "." + image_end_code
            member.avatar.save(avatar_name, file, save=True)
            member.save()

            http_response = {
                'status': 'success',
                'message': 'Change avatar success!',
            }
            return JsonResponse(http_response)

    return JsonResponse({'status': "ok"})


@login_required()
def change_card_id(request):
    if request.method == 'POST':
        new_card_id = request.POST['new_card_id']
        old_card_id = request.POST['old_card_id']
        member = Member.objects.get(card_id=old_card_id)
        member.card_id = new_card_id
        member.save()

        http_response = {
            'status': 'success',
            'message': 'Change card id success!',
        }
        return JsonResponse(http_response)


def server_authentication(request):
    if request.method == 'POST':
        card_id = request.POST['card_id']
        try:
            member = Member.objects.get(card_id=card_id)
            last_image_name = ''
            # save images to /tmp folder
            for face_key in request.FILES:
                last_image_name = face_key
                data = request.FILES[face_key]
                face = ImageFile(data)
                face_path = 'tmp/' + str(data)
                if default_storage.exists(face_path):
                    default_storage.delete(face_path)
                default_storage.save(face_path, face)

            # get result of predict list images
            list_predicts = face_recognize.recognition(member.recognize_label)
            # list_predicts = []
            if len(list_predicts):
                last_image_name = list_predicts[0][0]

            # check threshold
            result_auth = False
            f_name = None
            for file_name, conf in list_predicts:
                print(conf)
                if conf < member.threshold:
                    result_auth = True
                    f_name = file_name
                    break
            # publish result auth to mqtt topic /pas/mqtt/icse/auth
            result_auth_payload = 'OK' if result_auth else 'FAIL'
            mqtt.publish(const.MQTT_AUTH_TOPIC, result_auth_payload)
            print("ok")
            # get latest logs to check user in or out
            try:
                # TODO: check last log for new day, not last day
                last_log = Logs.objects.filter(member_id=member.id).latest('time_stamp')
                is_go_in = False if last_log.is_go_in else True
            except Logs.DoesNotExist:
                is_go_in = True

            member.is_in_lab = True if is_go_in else False
            member.save()

            # publish latest user scan to web browser
            latest_user_scan_payload = {
                'member_name': member.name,
                'state': 'Goes In' if is_go_in else 'Goes Out'
            }
            mqtt.publish(const.MQTT_LATEST_USER_SCAN, json.dumps(latest_user_scan_payload))

            # save logs
            log = Logs(
                time_stamp=timezone.now(),
                member=member,
                result_auth=result_auth,
                is_go_in=is_go_in,
            )
            f_name = f_name if result_auth else last_image_name
            file_path = os.path.join(const.TMP_FOLDER, f_name)
            file_data = File(open(file_path, 'rb'))
            log.image.save(f_name, file_data, save=True)
            log.save()
        except Member.DoesNotExist:
            print("member does not exist")
            mqtt.publish(const.MQTT_AUTH_TOPIC, 'FAIL')
            mqtt.publish(const.MQTT_MEMBER_DOES_NOT_EXIST, '1')
        return HttpResponse("POST request success")
    return HttpResponse("Not valid request type!")


@login_required()
def member_profile(request):
    member_id = request.GET['id']
    try:
        member = Member.objects.get(id=member_id)
    except Member.DoesNotExist:
        raise Http404("Member does not exist")
    moneys = Money.objects.filter(member_id=member_id)

    context = {
        'member': member,
        'moneys': moneys,
    }
    return render(request, 'pas/member/profile.html', context)


@login_required()
def train_face(request):
    member_id = request.GET['id']
    member = Member.objects.get(id=member_id)
    isTrain = request.GET['isTrain']
    if isTrain and isTrain == "true":
        # if not member.is_train:
        label = member.recognize_label
        images_trained = face_train.train(label)
        get_threshold = face_recognize.get_threshold(label)
        threshold = int(get_threshold[0])
        member.is_train = True
        member.threshold = threshold
        member.save()
        http_response = {
            'status': 'success',
            'message': 'Training success with {0} images -- '
                       'Get threshold success with {1} images'.format(images_trained, get_threshold[1]),
            'threshold': threshold,
        }

        # else:
        #     http_response = {
        #         'status': 'warning',
        #         'message': 'This member was had file train!'
        #     }
    else:
        member_label = member.recognize_label
        face_type = request.GET['type']
        get_faces_to_train.main(member_label, face_type)
        http_response = {
            'status': 'success',
            'message': 'Have taken enough 50 faces image!'
        }
    return JsonResponse(http_response)


@login_required()
def upload_video(request):
    if request.method == 'POST':
        id = request.POST['id']
        member = Member.objects.get(id=id)
        label = member.recognize_label
        video_data = request.FILES['video-train']
        video = ImageFile(video_data)
        video_name = request.POST['video-filename']
        video_path = 'video/' + str(label) + "/" + video_name
        if default_storage.exists(video_path):
            default_storage.delete(video_path)
        default_storage.save(video_path, video)

        number_of_faces = face_detection.face_detect(member.recognize_label)
        member.number_of_train_images += number_of_faces

        if member.number_of_train_images > 150:
            http_response = {
                'status': 'success',
                'message': 'Get enough {0} images'.format(member.number_of_train_images)
            }
        else:
            http_response = {
                'status': 'warning',
                'message': 'Get {0} images, please add more video!'.format(member.number_of_train_images)
            }

        return JsonResponse(http_response)
def server_log(request):
    zipped = zip(mqtt.member_in_server, mqtt.day)
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    logs_for_today = Logs.objects.filter(time_stamp__range=(today_min, today_max))
    context = {
            'logs':logs_for_today,
            'ngay':datetime.date.today().strftime("%B %d, %Y"),
            'zipdata': zipped
            }
    return render(request,'pas/server_log.html',context)

def server_log_stat(request):
    zipped = zip(mqtt.member_in_server,mqtt.day)
    date = request.POST['ngay']
    d = datetime.datetime.strptime(date, '%Y-%m-%d')
    today_min = datetime.datetime.combine(d, datetime.time.min)
    today_max = datetime.datetime.combine(d, datetime.time.max)
    logs_for_today = Logs.objects.filter(time_stamp__range=(today_min, today_max))
    context={
        'logs':logs_for_today,
        'ngay':d.strftime("%B %d, %Y"),
        'zipdata': zipped
    }
    return render(request,'pas/server_log.html',context)


