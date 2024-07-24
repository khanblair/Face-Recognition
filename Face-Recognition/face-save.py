import cv2
import tkinter as tk
from tkinter import *
import customtkinter
from tkinter import simpledialog
from PIL import Image, ImageTk
import os
import pyttsx3

# Setting my app theme
customtkinter.set_appearance_mode("System")

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier('face_detector.xml')

# Create the Tkinter window
root = customtkinter.CTk()
root.title("Face Detection and Registration/Login")

# Create a canvas to display the webcam feed
canvas = customtkinter.CTkCanvas(root, width=640, height=480)
canvas.place(relx=0.5, rely=0.6, anchor="center")
canvas.pack()

# Open the default webcam
cap = cv2.VideoCapture(0)

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Define a function to update the webcam feed
def update_frame():
    ret, img = cap.read()

    # Convert the OpenCV image to a Tkinter-compatible format
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)

    # Update the canvas with the new image
    canvas.create_image(0, 0, anchor=tk.NW, image=img)
    canvas.image = img

    # Schedule the next frame update
    root.after(10, update_frame)

# Define a function to perform face detection and recognition
def detect_and_recognize():
    ret, img = cap.read()

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(img, 1.1, 4)

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Check if the detected face matches a previously saved image
        for filename in os.listdir("."):
            if filename.endswith(".jpg"):
                name = os.path.splitext(filename)[0]
                saved_img = cv2.imread(filename)
                face_roi = img[y:y+h, x:x+w]
                saved_face_roi = saved_img[y:y+h, x:x+w]
                if cv2.compareHist(cv2.calcHist([face_roi], [0], None, [256], [0, 256]), cv2.calcHist([saved_face_roi], [0], None, [256], [0, 256]), cv2.HISTCMP_CORREL) > 0.8:
                    print(f"Welcome, {name}!")
                    engine.say(f"Welcome, {name}!")
                    engine.runAndWait()
                    return

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(img, 1.1, 4)

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Check if the detected face matches a previously saved image
        for filename in os.listdir("."):
            if filename.endswith(".jpg"):
                name = os.path.splitext(filename)[0]
                saved_img = cv2.imread(filename)
                face_roi = img[y:y+h, x:x+w]
                saved_face_roi = saved_img[y:y+h, x:x+w]
                if cv2.compareHist(cv2.calcHist([face_roi], [0], None, [256], [0, 256]), cv2.calcHist([saved_face_roi], [0], None, [256], [0, 256]), cv2.HISTCMP_CORREL) > 0.8:
                    print(f"Face already exists, please try again with a different name.")
                    engine.say(f"Face already exists, please try again with a different name.")
                    engine.runAndWait()
                    return

# Define a function to capture a photo and save it
def capture_photo():
    # Prompt the user for their name
    name = simpledialog.askstring("Registration", "Please enter your name:")
    if name is not None:
        ret, img = cap.read()

        # Detect faces in the captured image
        faces = face_cascade.detectMultiScale(img, 1.1, 4)

        # Check if a face is detected
        if len(faces) > 0:
            filename = f"{name}.jpg"
            # Check if the user is already registered
            if os.path.exists(filename):
                print(f"User {name} already registered. Please use the Login function.")
            else:
                # Check if the face in the current frame matches a previously saved image
                for (x, y, w, h) in faces:
                    face_roi = img[y:y+h, x:x+w]
                    for existing_filename in os.listdir("."):
                        if existing_filename.endswith(".jpg"):
                            existing_name = os.path.splitext(existing_filename)[0]
                            existing_img = cv2.imread(existing_filename)
                            existing_face_roi = existing_img[y:y+h, x:x+w]
                            if cv2.compareHist(cv2.calcHist([face_roi], [0], None, [256], [0, 256]), cv2.calcHist([existing_face_roi], [0], None, [256], [0, 256]), cv2.HISTCMP_CORREL) > 0.8:
                                print(f"Face already exists, please try again with a different name.")
                                engine.say(f"Face already exists, please try again with a different name.")
                                engine.runAndWait()
                                return
                cv2.imwrite(filename, img)
                print(f"Photo saved as {filename}")
        else:
            print("No face detected, photo not saved.")
    else:
        print("Registration cancelled.")

# Define a function to verify a user's identity
def verify_user():
    # Prompt the user for their name
    name = simpledialog.askstring("Login", "Please enter your name:")
    if name is not None:
        filename = f"{name}.jpg"
        if os.path.exists(filename):
            # Load the saved image and compare it with the current frame
            saved_img = cv2.imread(filename)
            ret, img = cap.read()
            faces = face_cascade.detectMultiScale(img, 1.1, 4)
            if len(faces) > 0:
                # Check if the face in the current frame matches the saved image
                for (x, y, w, h) in faces:
                    face_roi = img[y:y+h, x:x+w]
                    saved_face_roi = saved_img[y:y+h, x:x+w]
                    if cv2.compareHist(cv2.calcHist([face_roi], [0], None, [256], [0, 256]), cv2.calcHist([saved_face_roi], [0], None, [256], [0, 256]), cv2.HISTCMP_CORREL) > 0.8:
                        print(f"Welcome back, {name}!")
                        engine.say(f"Welcome back, {name}!")
                        engine.runAndWait()
                        return
                print("Face does not match the registered image. Please try again.")
            else:
                print("No face detected. Please try again.")
        else:
            print("User not found. Please register first.")
    else:
        print("Login cancelled.")

# Create a "Register" button
register_button = customtkinter.CTkButton(
                                            master=root, 
                                            text="Register", 
                                            width = 120,
                                            height = 30, 
                                            command=capture_photo
    )
register_button.place(relx=0.4, rely=0.9, anchor="center")

# Create a "Login" button
login_button = customtkinter.CTkButton(
                                            master=root, 
                                            text="Login", 
                                            width = 120,
                                            height = 30, 
                                            command=detect_and_recognize
    )
login_button.place(relx=0.6, rely=0.9, anchor="center")

# Start the main loop
update_frame()
root.mainloop()

