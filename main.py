from display import make_label
import webcam
from model import predict
import numpy as np
from win32api import GetSystemMetrics
from calibrate_ui import rel_pos_x, rel_pos_y

def main():
    cam = webcam.WebCam()
    cam_thread = cam.run()
    block = make_label(200)
    block.pack()
    x_coords = GetSystemMetrics(0)*np.array(rel_pos_x)
    y_coords = GetSystemMetrics(1)*np.array(rel_pos_y)
    while cam_thread.is_alive():
        data = cam.get_data()
        if not data is None:
            face, eyes, eye_frames = data
            prediction = predict(eye_frames, (*face, *eyes[0], *eyes[1]))
            x = int(np.sum(prediction*x_coords) - block.master.winfo_width()/2)
            y = int(np.sum(prediction*y_coords) - block.master.winfo_height()/2)
            block.master.geometry("+{0}+{1}".format(x, y))
        block.update()

if __name__ == "__main__":
    main()