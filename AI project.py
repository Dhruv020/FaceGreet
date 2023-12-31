import face_recognition 
import os, sys
import cv2
import numpy as np
import math
import pyttsx3
import datetime
speaker = pyttsx3.init('sapi5')
voices = speaker.getProperty('voices')
speaker.setProperty('voice',voices[0].id)
speaker.setProperty("rate", 120)

def wishMe():
    '''
    it will wish you as per time. to know what time is then  you have to use
    '''
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<12:
        speaker.say("Good Morning .")
    elif hour>=12 and hour<18:
        speaker.say("Good Afternoon .")

# Helper
def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True

    def __init__(self):
        self.encode_faces()

    def encode_faces(self):
        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f"faces/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)
        print(self.known_face_names)

    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            sys.exit('Video source not found...')
        personName = ""
        
        while True:
            ret, frame = video_capture.read()
            speaker.runAndWait()
            # Only process every other frame of video to save time
            if self.process_current_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]

                # Find all the faces and face encodings in the current frame of video
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                for face_encoding in self.face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"
                    confidence = '???'

                    # Calculate the shortest distance to face
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = face_confidence(face_distances[best_match_index])

                    self.face_names.append(f'{name} ({confidence})')
                    #mName: str = name.split(".")[0]

                    mName: str = name.split(".")[0]
                    if personName != mName:
                        wishMe()
                        wishMe()
                        speaker.say(f'''{mName} Welcome to DPS Poonae for a 2 day annual robotics event wherein teams of 13 different school learn to build robots and subsequently comepte to solve a challenge that employs concept of science, technology, engineering, math and computer science. 
                        Our schedule for todays event is:
                        730AM Registration at the registration counter and attendance.
                        Inaugration Ceremony at 8:00AM in the multipurpose hall. The robocon event will be conducted in the senior wing computer labs are located in the basement of the E 1 building. 
                        There will be a break from 10 30 AM to 11 AM for both robocon and AI bootcamp students in the basment and the senior wing quadrangle respectively. The training sessions
                        from both the mentors will continue in the allocated labs form 11 30 AM to 1 30 PM.
                        The models submitted by the participating student of robocon will be judged by our esteemed judges
                        from 1 30 PM to 2 30 PM.The event will end at 2 30PM''')
                        speaker.runAndWait()
                        personName = mName    
                    
                
                
            self.process_current_frame = not self.process_current_frame

            # Display the results
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Create the frame with the name
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom),       (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('Face Recognition', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run_recognition()