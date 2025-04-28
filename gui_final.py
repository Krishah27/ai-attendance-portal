# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 17:43:55 2025

@author: Krishna Shah
"""

import cv2
import os
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
import csv

# ------------ Face Recognition Setup ------------ #
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# ------------ User Mapping ------------ #
user_names = {
    11037933: "Khushi",
    93923144: "Krishna",
    69885452: "Param",
    60702745: "Shubham",
    91389023: "Yash",
    50220569: "yatri"
}

# ------------ Attendance Logger ------------ #
def mark_attendance(user_id):
    name = user_names.get(user_id, "Unknown")
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    
    if not os.path.exists("attendance.csv"):
        with open("attendance.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Date", "Time"])
    
    already_marked = False
    with open("attendance.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0] == str(user_id) and row[2] == date_str:
                already_marked = True
                break

    if not already_marked:
        with open("attendance.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([user_id, name, date_str, time_str])
        print(f"✔️ Attendance marked for {name} at {time_str}")

# ------------ GUI App ------------ #
class FaceAttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Karnavati University AI Attendance PORTAL")
        self.root.geometry("850x650")
        self.root.configure(bg="#f0f0f0")

        self.running = False
        self.cap = None

        # Video display
        self.video_label = tk.Label(self.root, bg="#ddd")
        self.video_label.pack(pady=20)

        # Status label
        self.status_label = tk.Label(self.root, text="", font=("Arial", 12), fg="green", bg="#f0f0f0")
        self.status_label.pack()

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="▶ Start", command=self.start_camera, width=12, bg="#4caf50", fg="white").grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="⏹ Stop", command=self.stop_camera, width=12, bg="#f44336", fg="white").grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="📸 Add New Face", command=self.add_new_face, width=15, bg="#2196f3", fg="white").grid(row=0, column=2, padx=10)
        tk.Button(btn_frame, text="📄 View Log", command=self.show_log, width=12, bg="#9c27b0", fg="white").grid(row=0, column=3, padx=10)
        tk.Button(btn_frame, text="❌ Exit", command=root.quit, width=12, bg="#777", fg="white").grid(row=0, column=4, padx=10)

    def start_camera(self):
        if not self.running:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # DirectShow for Windows webcam fix
            self.running = True
            self.update_frame()

    def stop_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.video_label.config(image='')

    def update_frame(self):
        if self.running:
            ret, frame = self.cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.2, 5)
                for (x, y, w, h) in faces:
                    roi_gray = gray[y:y+h, x:x+w]
                    id_, conf = recognizer.predict(roi_gray)
                    if conf < 80:
                        name = user_names.get(id_, "Unknown")
                        label = f"{name} ({round(100 - conf)}%)"
                        mark_attendance(id_)
                        self.status_label.config(text=f"✔️ Attendance marked for {name}")
                    else:
                        label = "Unknown"
                        self.status_label.config(text="⚠️ Unknown Face")

                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb_frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)

            self.root.after(10, self.update_frame)

    def show_log(self):
        if os.path.exists("attendance.csv"):
            os.system("start excel attendance.csv")
        else:
            messagebox.showinfo("Log", "No attendance records yet.")

    def add_new_face(self):
        name = simpledialog.askstring("Student Name", "Enter student's name:")
        id_ = simpledialog.askinteger("Student ID", "Enter student's ID:")

        if name and id_:
            dataset_path = "dataset"
            os.makedirs(dataset_path, exist_ok=True)
            cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

            count = 0
            while True:
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.2, 5)

                for (x, y, w, h) in faces:
                    count += 1
                    face_img = gray[y:y+h, x:x+w]
                    cv2.imwrite(f"{dataset_path}/User.{id_}.{count}.jpg", face_img)
                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

                cv2.imshow("Adding Face", img)
                if cv2.waitKey(1) == 27 or count >= 50:
                    break

            cam.release()
            cv2.destroyAllWindows()

            # Update user_names dictionary
            user_names[id_] = name
            messagebox.showinfo("Done", f"50 samples saved for {name}. Now run trainer.py to update recognizer.")

# ------------ Run GUI ------------ #
if __name__ == "__main__":
    root = tk.Tk()
    app = FaceAttendanceApp(root)
    root.mainloop()
