import tkinter, win32api, win32con, pywintypes
from PIL import Image, ImageTk

def make_label(size):
    window = tkinter.Tk()
    emoji = Image.open("chicken.png")
    emoji = ImageTk.PhotoImage(emoji.resize((size, size), Image.ANTIALIAS))
    label = tkinter.Label(image=emoji)
    label.image = emoji
    label.master.overrideredirect(True)
    label.master.geometry("+0+0")
    label.master.lift()
    label.master.wm_attributes("-topmost", True)
    label.master.wm_attributes("-disabled", True)
    label.master.wm_attributes("-transparentcolor", "white")

    remove_window(label)
    return label

def remove_window(block):
    hWindow = pywintypes.HANDLE(int(block.master.frame(), 16))
    exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
    win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)