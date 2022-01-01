rel_pos_x = .1, .9, .1, .9, .5, .25, .75, .5
rel_pos_y = .1, .1, .9, .9, .2, .5, .5, .8

if __name__ == '__main__':
    # importing tkinter for gui
    import tkinter as tk
    import webcam
    import data_controller

    cam = webcam.WebCam()
    cam.run()

    dc = data_controller.DataController()
    # dc.init_dataset()

    # creating window
    window = tk.Tk()
    
    # setting attribute
    window.attributes('-fullscreen', True)
    window.title("calibrate")

    file_name_label = tk.Label(window, text="file name", font=("", 30))
    file_name_label.place(relx = .5, rely = .4, anchor = "center")

    data_count = [0, 0, 0, 0, 0, 0, 0, 0]
    data_count_label = tk.Label(window, text=str(data_count), font=("", 30))
    data_count_label.place(relx = .5, rely = .6, anchor = "center")

    def save_data(label):
        cam_data = cam.get_data()
        if cam_data is None:
            file_name_label["text"] = "no data saved"
        else:
            file_name_label["text"] = dc.save_data(*cam_data, label)
            data_count[label] += 1
            data_count_label["text"] = str(data_count)
            print(data_count)


    # creating text labels to display on window screen
    for count in range(8):
        button = tk.Button(window, text=str(count))
        button.place(relx = rel_pos_x[count], rely = rel_pos_y[count], anchor = "center")
        if count == 0:
            button["command"] = lambda:save_data(0)
        elif count == 1:
            button["command"] = lambda:save_data(1)
        elif count == 2:
            button["command"] = lambda:save_data(2)
        elif count == 3:
            button["command"] = lambda:save_data(3)
        elif count == 4:
            button["command"] = lambda:save_data(4)
        elif count == 5:
            button["command"] = lambda:save_data(5)
        elif count == 6:
            button["command"] = lambda:save_data(6)
        elif count == 7:
            button["command"] = lambda:save_data(7)

    window.mainloop()