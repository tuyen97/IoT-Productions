import os

from enum import IntEnum

from server import settings

BC_SERVER = 'http://192.168.60.82:9090/'
# BC_SERVER = '192.168.60.238:8080/'
BC_API_ADD_USER = 'add_user_by_id/'
BC_API_DEL_USER = 'del_user_by_id/'
BC_API_CALCULATE_SALARY_USER = 'calculate_salary_users/'
BC_API_GET_SALARY_IN_DAY = 'get_salary_in_day'
BC_API_GET_SALARY_IN_PERIOD = 'get_salary_in_period'

TMP_FOLDER = os.path.join(settings.BASE_DIR, 'images/tmp/')
EIGENFACES_FOLDER = os.path.join(settings.BASE_DIR, 'pas/eigenfaces/')
FACE_TRAIN_FOLDER = os.path.join(settings.BASE_DIR, 'pas/member_images/')
FACE_CASCADE_PATH = os.path.join(settings.BASE_DIR, 'pas/haarcascade_frontalface_default.xml')

VIDEO_PATH = os.path.join(settings.BASE_DIR, 'images/video/')

TRAIN_FACES_FOLDER_NAME = 'train_faces/'
TEST_FACES_FOLDER_NAME = 'test_faces/'
MQTT_MEMBER_DOES_NOT_EXIST="pas/mqtt/member/does_not_exist"

NUMBER_COMPONENT = 200

MQTT_AUTH_TOPIC = "pas/mqtt/icse/auth"
MQTT_LATEST_USER_SCAN = 'pas/mqtt/server/latest_scan'


class MemberType(IntEnum):
    student = 1
    teacher = 2
