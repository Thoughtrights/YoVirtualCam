from cv2 import VideoCapture, imread, resize, cvtColor, COLOR_BGR2RGB, CAP_PROP_POS_FRAMES, INTER_AREA
from tkinter import Tk, Label
from tkinter.filedialog import askopenfilename
from tkinter import Button, StringVar, OptionMenu
from tkinter.ttk import Frame
from PIL import Image, ImageTk
from pyvirtualcam import PixelFormat, Camera
from pyautogui import screenshot
from numpy import array
mode = "Screen Broadcast"

def get_media():
	Tk().withdraw()
	return askopenfilename()

def select_mode(choice):
	if variable.get() == "Video Broadcast": global cap; cap = VideoCapture(get_media());
	if variable.get() == "Image Broadcast": global image; image = imread(get_media());
	global mode; mode=variable.get();

def screen_broadcast(mainWindow):
	mainWindow.destroy()
	cam = Camera(height=1080,width=1920,fps=60,fmt=PixelFormat.BGR)
	while True:
		if mode == "Screen Broadcast": frame = array(screenshot())
		if mode == "Video Broadcast": _, frame = cap.read()
		if mode == "Image Broadcast": frame = image;
		try:
			resized = resize(frame, (1920, 1080), interpolation=INTER_AREA)
			cam.send(resized)
		except:
			cap.set(CAP_PROP_POS_FRAMES, 0)	

def show_frame():
	if mode == "Screen Broadcast": frame = array(screenshot())
	if mode == "Video Broadcast": _, frame = cap.read()
	if mode == "Image Broadcast": frame = cvtColor(image, COLOR_BGR2RGB);
	try:
		imgtk = ImageTk.PhotoImage(image=Image.fromarray(frame).resize((760, 400)))
		lmain.imgtk = imgtk
		lmain.configure(image=imgtk)
		lmain.after(10, show_frame)
	except TypeError:
		cap.set(CAP_PROP_POS_FRAMES, 0)
		lmain.after(10, show_frame)	

mainWindow = Tk()
mainWindow.title("Yo VirtualCam Tool")
mainWindow.configure(bg="#47008a")
mainWindow.geometry('%dx%d+%d+%d' % (800,480,0,0))
mainWindow.resizable(0,0)
mainFrame = Frame(mainWindow)
mainFrame.place(x=20, y=20)
lmain = Label(mainFrame)
lmain.grid(row=0, column=0)

Broadcast = Button(mainWindow,text="Broadcast",font=("Constantia", 14),bg="#ffffff",width=20,height=1,highlightbackground="black",highlightthickness=2,bd=0)
Broadcast.configure(command= lambda: screen_broadcast(mainWindow))              
Broadcast.place(x=300,y=435)

Modes = ['Screen Broadcast','Video Broadcast', 'Image Broadcast']
variable = StringVar()
variable.set(Modes[0])
dropdown = OptionMenu(mainWindow,variable,*Modes,command=select_mode)
dropdown.place(x=650,y=435)

show_frame()
mainWindow.mainloop()  