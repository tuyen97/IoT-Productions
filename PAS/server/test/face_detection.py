import cv2

folder = 'faces/pas_face_'


def main():

    face_cascade = cv2.CascadeClassifier('../pas/haarcascade_frontalface_default.xml')
    # video_capture = cv2.VideoCapture(-1)
    video_capture = cv2.VideoCapture('../images/tmp/b.webm')

    w,h = 432, 240
    video_capture.set(3, w)
    video_capture.set(4, h)

    size = 4
    arr_faces = []
    number_of_faces = 4

    # while True:
    while video_capture.isOpened():
        # capture frame by frame
        ret, frame = video_capture.read()
        if not ret:
            break
        else:
            frame = cv2.flip(frame, 1, 0)
            mini_frame = cv2.resize(frame, (int(frame.shape[1] / size), int(frame.shape[0] / size)))
            faces = face_cascade.detectMultiScale(mini_frame)
            # draw a rectangle around the faces
            if len(faces) == 1:
                # time.sleep(1)
                (x, y, w, h) = [v * size for v in faces[0]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # print(len(arr_faces))
                sub_face = frame[y:y + h, x:x + w]
                FaceFileName = folder + str(10 + len(arr_faces)) + ".jpg"
                # cv2.imwrite(FaceFileName, sub_face)
                arr_faces.append(y)

            # cv2.imshow('Video', frame)

            # enter character 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
            # if cv2.waitKey(1) & 0xFF == ord('q') or len(arr_faces) >= number_of_faces:
                break

    # when everything is done, release the capture
    print("destroy....")
    video_capture.release()
    cv2.destroyAllWindows()

    return len(arr_faces)


if __name__ == "__main__":
    a = main()
    print(a)
