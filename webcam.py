import cv2
import numpy as np
import thread6
import face_detection
fd = face_detection.FaceDetector()

class WebCam:
    def __init__(self):
        # face and eyes represented with (x, y, w, h) tuples
        self.face = None
        self.eyes = [None, None]
        # eye frames represented as concatenated left/right eye frames
        self.eye_frames = None
        # new_frame is true if we have an unsaved frame available
        self.new_frame = False

    @thread6.threaded()
    def run(self):
        # initialize main webcam loop
        vc = cv2.VideoCapture(0)

        if vc.isOpened(): # try to get the first frame
            rval, frame = vc.read()
        else:
            raise Exception("Cannot get webcam input")

        while rval:
            # get video frame
            rval, frame = vc.read()

            # detect face, convert frame to gray scale
            face = fd.detect_face(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
            
            # check that face is not null
            if not face is None:
                self.face = face
                x, y, w, h = face
                # crop out face
                face_frame = frame[y:y+h, x:x+w]
                # draw rectangle around face
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)

                # detect eyes, represented as left, right tuple
                eyes = fd.detect_eyes(cv2.cvtColor(face_frame, cv2.COLOR_BGR2GRAY))

                # check that both eyes are not null
                if not any(map(lambda e: e is None, eyes)):
                    left = True
                    # eye cropout dimensions
                    dims = 50, 50
                    for eye in eyes:
                        ex, ey, ew, eh = eye
                        # ensures that frame crop is centered
                        offset = int((ew-dims[0])/2), int((eh-dims[1])/2)
                        # new coordinates relative to frame; prevent out of bounds relative to face_frame
                        nx, ny, nw, nh = x + ex + offset[0], y + ey + offset[1], dims[0], dims[1]
                        nx, ny = max(0, nx), max(0, ny)
                        nx, ny = min(nx, np.size(frame, 1)-nw), min(ny, np.size(frame, 0)-nh)
                        # copy array to rid of rectangle, also convert to gray scale
                        eye_frame = np.copy(cv2.cvtColor(frame[ny:ny+nh, nx:nx+nw], cv2.COLOR_BGR2GRAY))
                        if left:
                            left = False
                            self.eyes[0] = eye
                            self.eye_frames = eye_frame
                        else:
                            self.eyes[1] = eye
                            self.eye_frames = np.concatenate((self.eye_frames, eye_frame), axis=1)

                        # draw rectangle around eye using original coordinates
                        cv2.rectangle(face_frame, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 1)
                    
                    # uncomment to show eye_frames
                    # cv2.imshow("eye preview", self.eye_frames)
                    self.new_frame = True

            # show frame
            cv2.imshow("preview", frame)
            
            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                break

        vc.release()
        cv2.destroyAllWindows()
    
    def get_data(self):
        if not self.new_frame:    
            return None
        self.new_frame = False
        return self.face, self.eyes, self.eye_frames