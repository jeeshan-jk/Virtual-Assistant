# from sys import flags
# import time
# import cv2
# import pyautogui as p


# def AuthenticateFace():

#     flag = ""
#     # Local Binary Patterns Histograms
#     recognizer = cv2.face.LBPHFaceRecognizer_create()

#     recognizer.read('engine\\auth\\trainer\\trainer.yml')  # load trained model
#     cascadePath = "engine\\auth\\haarcascade_frontalface_default.xml"
#     # initializing haar cascade for object detection approach
#     faceCascade = cv2.CascadeClassifier(cascadePath)

#     font = cv2.FONT_HERSHEY_SIMPLEX  # denotes the font type


#     id = 2  # number of persons you want to Recognize


#     names = ['', 'Jeeshan','sushma']  # names, leave first empty bcz counter starts from 0


#     cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # cv2.CAP_DSHOW to remove warning
#     cam.set(3, 640)  # set video FrameWidht
#     cam.set(4, 480)  # set video FrameHeight

#     # Define min window size to be recognized as a face
#     minW = 0.1*cam.get(3)
#     minH = 0.1*cam.get(4)

#     # flag = True

#     while True:

#         ret, img = cam.read()  # read the frames using the above created object

#         # The function converts an input image from one color space to another
#         converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#         faces = faceCascade.detectMultiScale(
#             converted_image,
#             scaleFactor=1.2,
#             minNeighbors=5,
#             minSize=(int(minW), int(minH)),
#         )

#         for(x, y, w, h) in faces:

#             # used to draw a rectangle on any image
#             cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

#             # to predict on every single image
#             id, accuracy = recognizer.predict(converted_image[y:y+h, x:x+w])

#             # Check if accuracy is less them 100 ==> "0" is perfect match
#             if (accuracy < 100):
#                 id = names[id]
#                 accuracy = "  {0}%".format(round(100 - accuracy))
#                 flag = 1
#             else:
#                 id = "unknown"
#                 accuracy = "  {0}%".format(round(100 - accuracy))
#                 flag = 0

#             cv2.putText(img, str(id), (x+5, y-5), font, 1, (255, 255, 255), 2)
#             cv2.putText(img, str(accuracy), (x+5, y+h-5),
#                         font, 1, (255, 255, 0), 1)

#         cv2.imshow('camera', img)

#         k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
#         if k == 27:
#             break
#         if flag == 1:
#             break
            

#     # Do a bit of cleanup
    
#     cam.release()
#     cv2.destroyAllWindows()
#     return flag


# import cv2

# def AuthenticateFace():
#     flag = 0

#     recognizer = cv2.face.LBPHFaceRecognizer_create()
#     recognizer.read('engine\\auth\\trainer\\trainer.yml')

#     faceCascade = cv2.CascadeClassifier("engine\\auth\\haarcascade_frontalface_default.xml")
#     if faceCascade.empty():
#         print("❌ Haar cascade file not found")
#         return 0

#     font = cv2.FONT_HERSHEY_SIMPLEX

#     # Must match your dataset IDs
#     names = ['', 'Jeeshan', 'Sushma']

#     cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#     cam.set(3, 640)
#     cam.set(4, 480)

#     minW = 0.1 * cam.get(3)
#     minH = 0.1 * cam.get(4)

#     while True:
#         ret, img = cam.read()
#         if not ret:
#             print(" Camera not accessible")
#             break

#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#         faces = faceCascade.detectMultiScale(
#             gray,
#             scaleFactor=1.2,
#             minNeighbors=5,
#             minSize=(int(minW), int(minH)),
#         )

#         for (x, y, w, h) in faces:
#             cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

#             person_id, accuracy = recognizer.predict(gray[y:y+h, x:x+w])

#             if accuracy < 50:  # threshold for match
#                 name = names[person_id]
#                 conf_text = f"{round(100 - accuracy)}%"
#                 flag = 1
#             else:
#                 name = "Unknown"
#                 conf_text = f"{round(100 - accuracy)}%"
#                 flag = 0

#             cv2.putText(img, str(name), (x+5, y-5), font, 1, (255, 255, 255), 2)
#             cv2.putText(img, str(conf_text), (x+5, y+h-5), font, 1, (255, 255, 0), 1)

#         cv2.imshow('camera', img)

#         k = cv2.waitKey(10) & 0xff
#         if k == 27:  # ESC to quit
#             break
#         if flag == 1:
#             break

#     cam.release()
#     cv2.destroyAllWindows()
#     return flag




import cv2

def AuthenticateFace():
    flag = 0

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('engine/auth/trainer/trainer.yml')

    faceCascade = cv2.CascadeClassifier("engine/auth/haarcascade_frontalface_default.xml")
    if faceCascade.empty():
        print(" Haar cascade file not found")
        return 0

    font = cv2.FONT_HERSHEY_SIMPLEX

    # Must match your dataset IDs
    names = [ 'nandini', 'anusha','jeeshan']  # Extend if you add more users

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)
    cam.set(4, 480)

    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        ret, img = cam.read()
        if not ret:
            print("Camera not accessible")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

            person_id, accuracy = recognizer.predict(gray[y:y+h, x:x+w])

            if accuracy < 50:  # threshold for match
                if person_id < len(names):   
                    name = names[person_id]
                else:
                    name = f"ID-{person_id}"
                conf_text = f"{round(100 - accuracy)}%"
                flag = 1
            else:
                name = "Unknown"
                conf_text = f"{round(100 - accuracy)}%"
                flag = 0

            cv2.putText(img, str(name), (x+5, y-5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(conf_text), (x+5, y+h-5), font, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)

        k = cv2.waitKey(10) & 0xff
        if k == 27:  # ESC to quit
            break
        if flag == 1:  # Stop if recognized
            break

    cam.release()
    cv2.destroyAllWindows()
    return flag
