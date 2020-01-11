import face_recognition
import cv2
import numpy as np
import json
import time
import requests
import encodings.idna
import datetime
import os
# Setare Preset Imagini
OrtanAura_image = face_recognition.load_image_file("Mama.jpg")
OrtanAura_face_encoding = face_recognition.face_encodings(OrtanAura_image)[0]

OrtanAura2_image = face_recognition.load_image_file("MamaOchelari.jpg")
OrtanAura2_face_encoding = face_recognition.face_encodings(OrtanAura2_image)[0]

OrtanMihai_image = face_recognition.load_image_file("Eu.jpg")
OrtanMihai_face_encoding = face_recognition.face_encodings(OrtanMihai_image)[0]

OrtanMihai2_image = face_recognition.load_image_file("EuOchelari.jpg")
OrtanMihai2_face_encoding = face_recognition.face_encodings(OrtanMihai2_image)[0]

OrtanAndreea_image = face_recognition.load_image_file("andreea.jpg")
OrtanAndreea_face_encoding = face_recognition.face_encodings(OrtanAndreea_image)[0]

OrtanAndrei_image = face_recognition.load_image_file("tata.jpg")
OrtanAndrei_face_encoding = face_recognition.face_encodings(OrtanAndrei_image)[0]

# Vectori Cu Fete Si Nume Cunoscute
known_face_encodings = [
    OrtanAura_face_encoding,
    OrtanAura2_face_encoding,
    OrtanMihai_face_encoding, 
    OrtanMihai2_face_encoding,
    OrtanAndreea_face_encoding,
    OrtanAndrei_face_encoding
]
known_face_names = [
    "Ortan Aura",
    "Ortan Aura2",
    "Ortan Mihai",
    "Ortan Mihai",
    "Ortan Andreea",
    "Ortan Andrei"
]

# Initializare Variabile
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
shot = 0
time1 = 0
while True:

    # Luam Fiecare Frame Din Video
    video_capture = cv2.VideoCapture('http://admin:1111@192.168.1.108/tmpfs/auto.jpg')
    frame: object
    ret, frame = video_capture.read()

    # Micsorare frame pentru eficienta
    try:
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    except Exception as e:
        print(str(e))
     #transformare in RGB
    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        # Comparare Data De Baza Cu Imaginea Actuala
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # Verificare daca sunt sau nu 
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            if  name != "Ortan Mihai" and int(time.time()) > int(time1) + 5 :
                shot = shot + 1
            else:
                shot = 0
            if  shot == 2  :
                time1 = time.time()
                img_name = "opencv_frame_{}.jpg".format(time1)
                path = r'C:\Users\Info.MIHAI\Desktop\CameraSecurity\ShotLog'
                cv2.imwrite(os.path.join(path , img_name ), frame)
                shot = 0


            face_names.append(name)
    print(int(time.time()) - int(time1) + 5)
    process_this_frame = not process_this_frame


    # Afisare Rezultate
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scalare Inapoi A Imagini
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Desenare Dreptunghi In Jurul Fetei
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Desenare Nume
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    try:
        cv2.imshow('Video', frame)
    except Exception as e:
        print(str(e))

    # Pentru a opri , apasati 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
