import os
import shutil
import time
import csv
import cv2

class DataController:
    def init_dataset(self):
        # reset dataset folder
        if os.path.exists("dataset"):
            shutil.rmtree("dataset")
        os.makedirs("dataset/frames")

    def save_data(self, face, eyes, eye_frames, label):
        file_name = str(time.time()).replace(".", "_") + ".jpg"
        with open("dataset/data.csv", "a", encoding="UTF8", newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([*face, *eyes[0], *eyes[1], file_name, label])
        cv2.imwrite("dataset/frames/" + file_name, eye_frames)
        return file_name
        