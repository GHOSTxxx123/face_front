import os, secrets
from flask_login import login_required, logout_user, login_user, current_user
from flask import abort, session, Response, Flask
from read import app
from flask import render_template, send_from_directory, request, flash, url_for, redirect, jsonify
from PIL import Image
import cv2
import face_recognition
import numpy as np



def capture_by_frames():
    global camera

    camera = cv2.VideoCapture(1)

    image1 = face_recognition.load_image_file("C:\\Users\\Azam\\Desktop\\face_front\\read\\img1.jpg")
    face_encoding1 = face_recognition.face_encodings(image1, model='large')[0]


    image2 = face_recognition.load_image_file("C:\\Users\\Azam\\Desktop\\face_front\\read\\img_1.jpg")
    face_encoding2 = face_recognition.face_encodings(image2, model='large')[0]

    known_face_encodings = [
        face_encoding1,
        face_encoding2
    ]

    known_face_names = [
        "Негматов Аьзам",
        "Юсупов Мухаммедальсаид"
    ]

    running = True
        
    while running:
        ret, frame = camera.read()

        face_locations = face_recognition.face_locations(frame, number_of_times_to_upsample=1, model='cnn|hog')
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        try:
            face_encoding = face_encodings[0]
            top, right, bottom, left = face_locations[0]

            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
    
            if matches[best_match_index] == True: 
                cv2.rectangle(frame, (left, top), (right, bottom), (50, 205, 50), 2)
                name_user = known_face_names[best_match_index]
                print(name_user)

            elif matches[best_match_index] == False:

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        except:
            pass

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    return render_template('index.html')

@app.route('/stop')    
def stop():
    if camera.isOpened():
        camera.release()
    return render_template('stop.html')

@app.route('/video_capture')
def video_capture():
    return Response(capture_by_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

