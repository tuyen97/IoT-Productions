import cv2
import os

from . import const


def face_detect(label):
    video_path = os.path.join(const.VIDEO_PATH, str(label))

    face_cascade = cv2.CascadeClassifier(const.FACE_CASCADE_PATH)
    number_of_faces = 1

    folder_test = os.path.join(const.FACE_TRAIN_FOLDER, str(label), const.TEST_FACES_FOLDER_NAME)
    if not os.path.exists(folder_test):
        os.makedirs(folder_test)
    folder_train = os.path.join(const.FACE_TRAIN_FOLDER, str(label), const.TRAIN_FACES_FOLDER_NAME)
    if not os.path.exists(folder_train):
        os.makedirs(folder_train)

    for dirname, dirnames, filenames in os.walk(video_path):
        for filename in filenames:
            video = os.path.join(dirname, filename)
            print(video)

            video_capture = cv2.VideoCapture(video)

            w, h = 432, 240
            video_capture.set(3, w)
            video_capture.set(4, h)

            size = 4

            # while True:
            while video_capture.isOpened():
                # capture frame by frame
                ret, frame = video_capture.read()
                if ret:
                    frame = cv2.flip(frame, 1, 0)
                    mini_frame = cv2.resize(frame, (int(frame.shape[1] / size), int(frame.shape[0] / size)))
                    faces = face_cascade.detectMultiScale(mini_frame)
                    if len(faces) == 1:
                        (x, y, w, h) = [v * size for v in faces[0]]
                        sub_face = frame[y:y + h, x:x + w]
                        if number_of_faces < 40:
                            folder = folder_test
                        else:
                            folder = folder_train
                        FaceFileName = folder + str(10 + number_of_faces) + ".jpg"
                        cv2.imwrite(FaceFileName, sub_face)
                        number_of_faces += 1

                    # enter character 'q' to quit
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    break
            # when everything is done, release the capture
            print("destroy...., number of images: {0}".format(number_of_faces))
            video_capture.release()

    return number_of_faces


if __name__ == "__main__":
    face_detect(1)
