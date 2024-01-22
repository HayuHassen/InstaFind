import tkinter as tk 
import os 
from PIL import Image, ImageTk 
from PIL import Image
import cv2
import numpy as np
import face_recognition
import glob

class WebcamApp:
    def __init__(self,window):
        self.known_face_encodings = []
        self.known_face_names = []
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
        self.face_names=[]



    def update_webcam(self):
        ret,frame= self.video_capture.read()

        if ret:
            self.current_image= Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
            self.photo=ImageTk.PhotoImage(self.current_image)
            self.canvas.create_image(0,0,image=self.photo,anchor=tk.NW)
            self.window.after(15,self.update_webcam)
    def load_encoding_images(self, images_path):
        # Load Images
        images_path = glob.glob(os.path.join(images_path, "*.*"))

        print("{} encoding images found.".format(len(images_path)))


        # Store image encoding and names

        for img_path in images_path:
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Get the filename only from the initial file path.
            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)
        # Get encoding
            img_encoding = face_recognition.face_encodings(rgb_img)[0]

        # Store file name and file encoding
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(filename)

    def detect_known_faces(self, frame):
        small_frame = np.array(frame)
        # Find all the faces and face encodings in the current frame of video
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(rgb_small_frame)


        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            self.face_names.append(name)
            print(self.face_names)



    def download_image(self):
        if self.current_image is not None:
            self.current_image.show()
            numpy_image = np.array(self.current_image )
            ref = cv2.imread(r'Faces/Hayu.jpg')
            ref_color = cv2.cvtColor(ref, cv2.COLOR_BGR2RGB)
            current_image_color= cv2.cvtColor(numpy_image,cv2.COLOR_BGR2RGB)
            ref_encoding = face_recognition.face_encodings(ref_color)[0]
            current_image_encoding = face_recognition.face_encodings(numpy_image )[0]
            result = face_recognition.compare_faces([current_image_encoding],ref_encoding)
            print("Result:", result)
            self.load_encoding_images('Faces/')
            self.detect_known_faces(self.current_image)










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
