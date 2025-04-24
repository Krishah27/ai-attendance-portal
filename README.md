# AI Attendance Portal 🎓📷

A Python-based face recognition attendance system utilizing OpenCV and Haar Cascade Classifier. This system captures live video, detects faces, and marks attendance automatically with a timestamp.

## 🚀 Features

- 🔍 Real-time face detection using webcam
- 🧠 Face recognition with OpenCV’s LBPH algorithm
- 📅 Auto attendance marking with date and time
- 💾 Attendance saved in CSV files
- 🖥️ Standalone GUI (`.exe` included)
- 🧪 Face dataset generation + model training

## 🧰 Technologies Used

- Python
- OpenCV
- Haar Cascade Classifier
- LBPH Face Recognizer
- CSV for attendance storage


## 🚀 How to Run

1. **Clone the Repository**

    git clone https://github.com/Krishah27/ai-attendance-portal.git
   cd ai-attendance-portal

2. **Install Dependencies**
   
pip install -r requirements.txt

3. **Run the Application**

python gui_attendance.py

Alternatively, you can run the executable :

Double-click gui_attendance.exe

## 🧠 How It Works

Face Data Collection – Capture face images using webcam and store them under /dataset.

Training – Train the LBPH recognizer using trainer.yml.

Live Recognition – Run the GUI app to detect and recognize faces in real time.

Attendance Logging – Automatically logs recognized users into a .csv file.

## 📝 Future Improvements

Add face mask detection

Cloud integration for attendance reports

Multiple camera support

Android version for portable use

## 🛠️ Tech Stack

- **Language**: Python
- **Libraries**: OpenCV, NumPy
- **Model**: Haar Cascade (Detection) + LBPH (Recognition)
- **GUI**: Tkinter (converted to `.exe`)
- **Packaging**: PyInstaller

## 👥 Developed By

Made with ❤️ by: <br>
<br>
Krishah27 <br>
Khushimalani01

Together, we designed and built this project as a part of our AI initiative to make attendance smarter, faster, and contactless.

## 🤝 Let’s Connect
Have ideas, feedback, or want to collaborate with us?
Reach out to us on Linkedln — we’d love to hear from you! <br>
<br>
Krishna Shah : https://www.linkedin.com/in/krishna-shah-9a1a27316?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app <br>
Khushi Malani : https://www.linkedin.com/in/khushi-malani-37aa1731b?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app

## “Alone we can do so little; together we can do so much.” – Helen Keller

Thanks for exploring the AI Attendance Portal — built with purpose, code, and teamwork. 🧠💻👥
