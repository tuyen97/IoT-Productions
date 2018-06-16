import cv2, os, sys

from . import const

TMP_FOLDER = const.TMP_FOLDER
EIGENFACES_FOLDER = const.EIGENFACES_FOLDER
FACE_CASCADE_PATH = const.FACE_CASCADE_PATH

# from server import  settings
# TMP_FOLDER = os.path.join(settings.BASE_DIR, 'tmp/')
# EIGENFACES_FOLDER = os.path.join(settings.BASE_DIR, 'pas/eigenfaces/')
# FACE_CASCADE_PATH = os.path.join(settings.BASE_DIR, 'pas/haarcascade_frontalface_default.xml')

width_resize = 100
height_resize = 100


def recognition(label, is_get_threshold=False):
    if is_get_threshold:
        walk_folder = os.path.join(const.FACE_TRAIN_FOLDER, str(label), const.TEST_FACES_FOLDER_NAME)
    else:
        walk_folder = TMP_FOLDER
    faceCascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
    model_path = os.path.join(EIGENFACES_FOLDER, str(label) + ".yml")
    recognizer = cv2.face.EigenFaceRecognizer_create(const.NUMBER_COMPONENT)
    recognizer.read(model_path)

    result = []

    for dirname, dirnames, filenames in os.walk(walk_folder):
        for filename in filenames:
            try:
                image_path = os.path.join(dirname, filename)
                image = cv2.imread(image_path)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(image)

                if len(faces) == 1:
                    for (x, y, w, h) in faces:
                        # face_image = cv2.resize(image, (width_resize, height_resize))
                        face_image = cv2.resize(image[y:y + h, x:x + w], (width_resize, height_resize))
                        label_predicted, conf = recognizer.predict(face_image)
                        if is_get_threshold:
                            result.append(conf)
                        else:
                            result.append((filename, conf))
                        print("{0} - {1}".format(filename, conf))
            except IOError:
                print("I/O error({0}): {1}")
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

    return result


def get_threshold(label):
    list_conf = recognition(label, is_get_threshold=True)
    print('number of image test to get threshold: {0}'.format(len(list_conf)))
    # threshold = sum(list_conf) / len(list_conf)
    threshold = max(list_conf)
    print('threshold - {0}'.format(threshold))
    return (threshold, len(list_conf))


if __name__ == '__main__':
    recognition(1)
