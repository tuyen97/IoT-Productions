import cv2
import os, time

from . import const

FACE_TRAIN_FOLDER = const.FACE_TRAIN_FOLDER
FACE_CASCADE_PATH = const.FACE_CASCADE_PATH
TMP_FOLDER = const.TMP_FOLDER


def main(label, type):

    sub_folder = FACE_TRAIN_FOLDER + str(label) + "/"
    if not os.path.exists(sub_folder):
        os.makedirs(sub_folder)
    type_folder = sub_folder + "/" + type
    if not os.path.exists(type_folder):
        os.makedirs(type_folder)

    face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
    video_capture = cv2.VideoCapture(-1)

    w,h = 432, 240
    video_capture.set(3, w)
    video_capture.set(4, h)

    size = 4
    arr_faces = []
    number_of_faces = 50

    while True:
        # capture frame by frame
        ret, frame = video_capture.read()
        frame = cv2.flip(frame, 1, 0)
        mini_frame = cv2.resize(frame, (int(frame.shape[1] / size), int(frame.shape[0] / size)))
        faces = face_cascade.detectMultiScale(mini_frame)
        # draw a rectangle around the faces
        if len(faces) == 1:
            (x, y, w, h) = [v * size for v in faces[0]]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # if y and not y in arr_faces:
            #     print(len(arr_faces))
            #     sub_face = frame[y:y + h, x:x + w]
            #     face_file_name = type_folder + "/" + str(10 + len(arr_faces)) + ".jpg"
            #     cv2.imwrite(face_file_name, sub_face)
            #     arr_faces.append(y)
            print(len(arr_faces))
            sub_face = frame[y:y + h, x:x + w]
            face_file_name = type_folder + "/" + str(10 + len(arr_faces)) + ".jpg"
            cv2.imwrite(face_file_name, sub_face)
            arr_faces.append(y)
        # display the resulting frame
        # cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or len(arr_faces) >= number_of_faces:
            break

    # when everything is done, release the capture
    print("destroy....")
    video_capture.release()
    # cv2.destroyAllWindows()


if __name__ == "__main__":
    print("run main...")

    # main(0)
