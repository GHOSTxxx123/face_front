import os, secrets
from flask_login import login_required, logout_user, login_user, current_user
from flask import abort, session, Response, Flask
#from read import app
from flask import render_template, send_from_directory, request, flash, url_for, redirect, jsonify
from PIL import Image
import cv2
import face_recognition
import numpy as np
from threading import Thread

global name_user

name_user = "Unkonw"

class qwe(Thread):
    def __init__(self):
        super().__init__()


    def run(self):
        global camera
        global name_user
        
        # "rtsp://admin:canerce123!@192.168.1.13:554/media/video1"
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
                #right = face_locations[0][1]
                #bottom = face_locations[0][2]
                #left = face_locations[0][3]
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
        
                if matches[best_match_index] == True: 
                    #print(known_face_names[best_match_index])
                    cv2.rectangle(frame, (left, top), (right, bottom), (50, 205, 50), 2)
                    name_user = known_face_names[best_match_index]
                    camera.release()
                elif matches[best_match_index] == False:

                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            except:
                pass

            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 


# @app.route('/logout/')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('sign_in'))

# @app.route('/sign_in/', methods=('GET', 'POST'))
# def sign_in():
#     form = Sign_in()
#     if form.validate_on_submit():
#         user = db.session.query(User).filter(User.gmail == form.gmail.data).first()
#         #password = db.session.query(User).filter(User.pass_hash == form.password.data).first()
#         if user and user.pass_hash == form.password.data:
#             login_user(user, remember=form.remember.data)
#             return redirect(url_for('index'))

#     return render_template('sign_in.html', form=form)


# @app.route('/sign_up/', methods=['POST', 'GET'])
# def sign_up():
#     form = Sign_up()
#     if form.validate_on_submit():
#         user = User(name=form.name.data,
#                     firstname=form.firstname.data,
#                     gmail=form.gmail.data,
#                     pass_hash=form.password.data)
#         db.session.add(user)
#         db.session.commit()        
#         return redirect(url_for('sign_in'))
#     return render_template('sign_up.html', form=form)
    # global camera
    # camera = cv2.VideoCapture(0)
    # while True:
    #     success, frame = camera.read()  # read the camera frame
    #     # detector=cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')
    #     # faces=detector.detectMultiScale(frame,1.2,6)
    #      #Draw the rectangle around each face
    #     # for (x, y, w, h) in faces:
    #     #     cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)


app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/start',methods=['POST'])
def start():
    return render_template('index.html', name=name_user)
@app.route('/stop',methods=['POST'])    
def stop():
    if camera.isOpened():
        camera.release()
    return render_template('stop.html')
@app.route('/video_capture')
def video_capture():
    second = qwe()
    second.daemon = True
    data = second.start()
    return Response(data, mimetype='multipart/x-mixed-replace; boundary=frame')



app.run()

# @app.before_first_request
# def create_tables():
#     #app.app_context().push()
#     db.create_all()