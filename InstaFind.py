import tkinter as tk 
import os 
from PIL import Image, ImageTk 
from PIL import Image
import cv2
import numpy as np
import face_recognition
class WebcamApp:
    def __init__(self,window):
        self.window=window
        self.window.title('InstaFind')
        self.video_capture= cv2.VideoCapture(0)
        self.current_image=None
        self.canvas= tk.Canvas(window, width=640, height= 480)
        self.canvas.pack()
        self.update_webcam()
        self.frame1= tk.Frame(window,width=640,height=480,background='#405DE6')
        self.frame1.pack()
        self.cheese_button= tk.Button(self.frame1, text= "Cheese!", command= self.download_image)
        self.cheese_button.place(x=300,y=5)
    def update_webcam(self):
        ret,frame= self.video_capture.read()

        if ret:
            self.current_image= Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
            self.photo=ImageTk.PhotoImage(self.current_image)
            self.canvas.create_image(0,0,image=self.photo,anchor=tk.NW)
            self.window.after(15,self.update_webcam)

    def download_image(self):
        if self.current_image is not None:
           self.current_image.show()
           numpy_image= np.array(self.current_image)
           ref= cv2.imread(r'Faces/Hayu Refrence.jpg')
           ref_color = cv2.cvtColor(ref, cv2.COLOR_BGR2RGB)
           current_image_color=cv2.cvtColor(numpy_image,cv2.COLOR_BGR2RGB)
           ref_encoding = face_recognition.face_encodings(ref_color)[0]
           current_image_encoding = face_recognition.face_encodings(current_image_color)[0]
           result = face_recognition.compare_faces([current_image_encoding], ref_encoding)
           print("Result:", result)







root=tk.Tk()
app= WebcamApp(root)    
root.mainloop()

'''
self.ref_cv= cv2.imread("Hayu Refrence.jpg")
self.ref_pil=Image.open('Hayu Refrence.jpg')
self.ref_pil.show()
self.ref_encoding = face_recognition.face_encodings(self.ref_color)[0]
self.current_image_encoding = face_recognition.face_encodings(self.current_image)[0]
self.result = face_recognition.compare_faces([self.current_image_encoding], self.ref_encoding)
print("Result:", self.result)
'''
