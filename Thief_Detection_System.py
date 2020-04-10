#Identifying thiefs or suspicious people using face recognition technology
import face_recognition # Face Recognition Module by Adam Geitgey
import cv2 #OpenCV
import numpy as np

# PLEASE NOTE: This requires OpenCV (the `cv2` library) to be installed to read from your webcam.

# Get a reference to webcam
video_capture = cv2.VideoCapture(0)

# Loading pictures of the specific people who have access to enter
# The image files specified in load_image_file() function refers to image location on the pc where program was developed, need to change for each pc
accesed_member1_image = face_recognition.load_image_file("/home/laikehan13/Downloads/my_picture.jpg")
accesed_member1_face_encoding = face_recognition.face_encodings(accesed_member1_image)[0] # Face encoding returns a list of length 1
accesed_member2_image = face_recognition.load_image_file("/home/laikehan13/Downloads/ganesh2.JPG")
accesed_member2_face_encoding = face_recognition.face_encodings(accesed_member2_image)[0]

# Array of face encodings of members having access to enter
known_face_encodings = [
    accesed_member1_face_encoding,
    accesed_member2_face_encoding,
]
known_face_names = [
    "Ganesh Nukala",
    "Ganesh Nukala"
]
sms_limit=0
while True:
    # Grabs the video frame
    ret, frame = video_capture.read()

    # Converting the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Finding all the faces and face enqcodings in the frame of video to identify suspicious people
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop through each face in this frame of video
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the authorized face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unauthorized Suspicious Person"
        # if True in matches: Does Nothing as the Person is authorized 
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        if(name=='Unauthorized Suspicious Person'):
            print('Suspicious Person near the Vault')
            sms_limit+=1
        if sms_limit%5==0 and name=='Unauthorized Suspicious Person':
            print('Thief detected')
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
