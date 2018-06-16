#!/usr/bin/python

# Import the required modules
import cv2, os, sys
import numpy as np

from . import const

FACE_CASCADE_PATH = const.FACE_CASCADE_PATH
FACE_TRAIN_FOLDER = const.FACE_TRAIN_FOLDER
EIGENFACES_FOLDER = const.EIGENFACES_FOLDER
TEST_FACES_FOLDER_NAME = const.TEST_FACES_FOLDER_NAME

# from server import  settings
# EIGENFACES_FOLDER = os.path.join(settings.BASE_DIR, 'pas/eigenfaces/')
# FACE_TRAIN_FOLDER = os.path.join(settings.BASE_DIR, 'pas/faces_train/')
# FACE_CASCADE_PATH = os.path.join(settings.BASE_DIR, 'pas/haarcascade_frontalface_default.xml')
# TEST_FACES_FOLDER_NAME = 'test_faces'


width_resize = 100
height_resize = 100


def get_images_and_labels(label, faceCascade):
    path_faces = os.path.join(FACE_TRAIN_FOLDER, str(label), const.TRAIN_FACES_FOLDER_NAME)
    images = []
    labels = []
    for dirname, dirnames, filenames in os.walk(path_faces):
        if dirname != os.path.join(path_faces, TEST_FACES_FOLDER_NAME) and filenames:
            for filename in filenames:
                try:
                    image_path = os.path.join(dirname, filename)
                    image = cv2.imread(image_path)
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                    images.append(cv2.resize(image, (width_resize, height_resize)))
                    labels.append(label)

                    # faces = faceCascade.detectMultiScale(image)
                    # #
                    # if len(faces) == 1:
                    #     for (x, y, w, h) in faces:
                    #         images.append(cv2.resize(image[y:y + h, x:x + w], (width_resize, height_resize)))
                    #         labels.append(label)
                except IOError:
                    print("I/O error({0}): {1}")
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    raise
    return images, labels


def train(label):
    faceCascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
    images, labels = get_images_and_labels(label, faceCascade)
    print("number image trained: ", len(images))

    recognizer = cv2.face.EigenFaceRecognizer_create(const.NUMBER_COMPONENT)
    recognizer.train(images, np.array(labels))
    recognizer.save(os.path.join(EIGENFACES_FOLDER, str(label) + ".yml"))
    return len(images)


if __name__ == '__main__':
    path_train = 1
    train(path_train)
