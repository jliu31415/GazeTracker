import cv2
import numpy as np
# path to face detection data
cascPath = "./Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml"
eyePath = "./Lib/site-packages/cv2/data/haarcascade_eye.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
eyeCascade = cv2.CascadeClassifier(eyePath)

class FaceDetector:
    def detect_face(self, img):
        # use face detection library
        faces = faceCascade.detectMultiScale(
            img,
            scaleFactor=1.1,
            minNeighbors=6,
            minSize=(50, 50),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # return None if no faces detected
        if (len(faces) == 0):
            return None
        return faces[0]
    
    def detect_eyes(self, img):
        eyes = eyeCascade.detectMultiScale(
            img,
            scaleFactor=1.1,
            minNeighbors=8,
            minSize=(10, 10)
        )

        width = np.size(img, 1) # get face frame width
        height = np.size(img, 0) # get face frame height
        left_eye, right_eye = None, None
        for eye in eyes:
            ex, ey, ew, eh = eye
            eye_center = ex+ew/2, ey+eh/2
            # skip if eye detected in bottom half of face
            if eye_center[1] > height/2:
                continue
            if eye_center[0] < width/2:
                left_eye = eye
            else:
                right_eye = eye
        return left_eye, right_eye