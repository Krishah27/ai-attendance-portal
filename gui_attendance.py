# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 23:28:21 2025

@author: Krishna Shah
"""

import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import os
import datetime
import csv

# ------------------ Face Recognizer Load ------------------ #
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Sample dictionary for user info - replace with real names and IDs
user_names = {
    11037933: "khushi",
    93923144: "krishna",
    69885452: "param",
    60702745: "shubham",
    91389023: "yash"
    # add more if needed
}


# ------------------ Attendance Logger ------------------ #
def mark_attendance(user_id):
    name = user_names.get(user_id, "Unknown")
    time_now = datetime.datetime.now().strftime("%H:%M:%S")
    date_now = datetime.datetime.now().strftime("%Y-%m-%d")

    already_marked = False
    if os.path.exists('attendance.csv'):
        with open('attendance.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == str(user_id) and row[2] == date_now:
                    already_marked = True
                    break

    if not already_marked:
        with open('attendance.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([user_id, name, date_now, time_now])
            print(f"✔️ Attendance marked for {name} at {time_now}")

# ------------------ GUI ------------------ #
class FaceAttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Face Attendance Portal")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.video_frame = tk.Label(self.root, bg="#cccccc")
        self.video_frame.pack(padx=10, pady=10)

        self.info_label = tk.Label(self.root, text="Press 'Start' to begin", font=("Helvetica", 14), bg="#f0f0f0")
        self.info_label.pack(pady=5)

        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="▶ Start", command=self.start_camera, width=12, bg="#4caf50", fg="white").pack(side="left", padx=10)
        tk.Button(btn_frame, text="⏹ Stop", command=self.stop_camera, width=12, bg="#f44336", fg="white").pack(side="left", padx=10)
        tk.Button(btn_frame, text="📄 View Log", command=self.show_log, width=12, bg="#2196f3", fg="white").pack(side="left", padx=10)
        tk.Button(btn_frame, text="❌ Exit", command=root.quit, width=12, bg="#777", fg="white").pack(side="left", padx=10)

        self.running = False
        self.cap = None

    def start_camera(self):
        if not self.running:
            self.cap = cv2.VideoCapture(0)
            self.running = True
            self.update_frame()

    def stop_camera(self):
        if self.running:
            self.running = False
            if self.cap:
                self.cap.release()
            self.video_frame.config(image='')

    def update_frame(self):
        if self.running:
            ret, frame = self.cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

                for (x, y, w, h) in faces:
                    roi_gray = gray[y:y+h, x:x+w]
                    user_id, confidence = recognizer.predict(roi_gray)
                    if confidence < 80:
                        name = user_names.get(user_id, "Unknown")
                        mark_attendance(user_id)
                        label = f"{name} ({round(100 - confidence)}%)"
                    else:
                        label = "Unknown"

                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_frame.imgtk = imgtk
                self.video_frame.configure(image=imgtk)

            self.root.after(10, self.update_frame)

    def show_log(self):
        if os.path.exists("attendance.csv"):
            os.system("start excel attendance.csv")  # Opens in Excel (Windows)
        else:
            messagebox.showinfo("Log", "No attendance recorded yet.")

# ------------------ Run App ------------------ #
if __name__ == "__main__":
    root = tk.Tk()
    app = FaceAttendanceApp(root)
    root.mainloop()
