import cv2
import os
from shutil import copyfile


# Class that takes care of the openCv features
class Camera():

    # Constructor...
    def __init__(self, frames):
        self.frames = frames
        self.cap = cv2.VideoCapture(0)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.writer = cv2.VideoWriter('myVideo.mp4', cv2.VideoWriter_fourcc(*'mp4v'), self.frames, (self.width, self.height))
        self.face_cascade = cv2.CascadeClassifier("./haarcascades/haarcascade_frontalface_default.xml")

    # Face detection function
    def detect_face(self, img):
        face_img = img.copy()
        found = False
        face_rects = self.face_cascade.detectMultiScale(face_img, scaleFactor=1.2, minNeighbors=5)
        for(x,y,w,h) in face_rects:
            if x > 0:
                found = True
            cv2.rectangle(face_img, (x, y), (x+w, y+h), (255, 255, 255), 2)
        return face_img, found

    # Frame generation for Browser streaming with Flask...
    def get_frame(self):
        frames = open("stream.jpg", 'wb+')
        s, img = self.cap.read()
        new_img, found = self.detect_face(img)
        if s:  # frame captures without errors...
            cv2.imwrite("stream.jpg", new_img)
            if found:
                cv2.imwrite("saved_pic/cap_pic.jpg", img)  # Save image as jpg
            elif os.path.isfile("saved_pic/cap_pic.jpg"):
                os.remove("saved_pic/cap_pic.jpg")

        return frames.read()

    # Captures the video being streamed from the camera
    def captureVideo(self, do_rec):
        frames = open("stream.jpg", 'wb+')
        s, img = self.cap.read()
        if s:
            cv2.imwrite("stream.jpg", img)
            if do_rec:
                self.writer.write(img)

        return frames.read()

    # Ends the video feed.
    def end_video(self):
        self.cap.release()
        self.writer.release()

    # Saves the video
    def save_video(self):
        # self.end_video()
        self.writer.release()
        copyfile("myVideo.mp4", "saved_vid/myVideo.mp4")

