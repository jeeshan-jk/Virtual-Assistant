# import cv2
# import numpy as np
# from PIL import Image #pillow package
# import os

# path = 'engine\\auth\\samples' # Path for samples already taken

# recognizer = cv2.face.LBPHFaceRecognizer_create() # Local Binary Patterns Histograms
# detector = cv2.CascadeClassifier("engine\\auth\\haarcascade_frontalface_default.xml")
# #Haar Cascade classifier is an effective object detection approach


# def Images_And_Labels(path): # function to fetch the images and labels

#     imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
#     faceSamples=[]
#     ids = []

#     for imagePath in imagePaths: # to iterate particular image path

#         gray_img = Image.open(imagePath).convert('L') # convert it to grayscale
#         img_arr = np.array(gray_img,'uint8') #creating an array

#         id = int(os.path.split(imagePath)[-1].split(".")[1])
#         faces = detector.detectMultiScale(img_arr)

#         for (x,y,w,h) in faces:
#             faceSamples.append(img_arr[y:y+h,x:x+w])
#             ids.append(id)

#     return faceSamples,ids

# print ("Training faces. It will take a few seconds. Wait ...")

# faces,ids = Images_And_Labels(path)
# recognizer.train(faces, np.array(ids))

# recognizer.write('engine\\auth\\trainer\\trainer.yml')  # Save the trained model as trainer.yml

# print("Model trained, Now we can recognize your face.")




import cv2
import numpy as np
from PIL import Image
import os

path = 'engine\\auth\\samples'

# Make sure trainer folder exists
os.makedirs("engine\\auth\\trainer", exist_ok=True)

# Load recognizer (requires opencv-contrib-python)
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("engine\\auth\\haarcascade_frontalface_default.xml")

if detector.empty():
    print(" Could not load Haar Cascade")
    exit()

def Images_And_Labels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.jpg')]
    faceSamples=[]
    ids = []

    for imagePath in imagePaths:
        gray_img = Image.open(imagePath).convert('L')
        img_arr = np.array(gray_img, 'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_arr)

        for (x,y,w,h) in faces:
            faceSamples.append(img_arr[y:y+h, x:x+w])
            ids.append(id)

    return faceSamples, ids

print("Training faces. It will take a few seconds. Wait ...")

faces, ids = Images_And_Labels(path)

if len(faces) == 0:
    print(" No faces found in samples folder. Did you run sample.py first?")
    exit()

recognizer.train(faces, np.array(ids))
recognizer.write('engine\\auth\\trainer\\trainer.yml')

print(" Model trained. Saved as trainer.yml")
