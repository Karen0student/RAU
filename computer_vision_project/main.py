import cv2 #pip install opencv-python
import os
import shutil # move file from directories
import threading
from datetime import datetime
from deepface import DeepFace

# This is to pull the information about what each object is called
classNames = []
classFile = "Resources/coco.names"
with open(classFile, "rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

# This is to pull the information about what each object should look like
configPath = "Resources/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "Resources/frozen_inference_graph.pb"
faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")

# This is some set up values to get good results
net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def capture_increase_size(x, y, w, h, img):
 # Increaseing crop size safely
    if w < 50 and h < 100:
        new_x = max(x - 50, 0)
        new_w = min(w + 100, img.shape[1] - new_x)
        new_y = max(y - 50, 0)
        new_h = min(h + 100, img.shape[0] - new_y)
        person_crop = img[new_y:new_y + new_h, new_x:new_x + new_w]
    elif w < 50 and h >= 100:
        new_x = max(x - 50, 0)
        new_w = min(w + 100, img.shape[1] - new_x)
        person_crop = img[y:y + h, new_x:new_x + new_w]
    elif h < 100 and w >= 50:
        new_y = max(y - 50, 0)
        new_h = min(h + 100, img.shape[0] - new_y)
        person_crop = img[new_y:new_y + new_h, x:x + w]
    else:
        person_crop = img[y:y + h, x:x + w]
    
    return person_crop

def capture_analyze_save(img, persons_path, faces_path, emotions_path):
    # Detect objects
    img_clear = img.copy()
    img_rectangle, objectInfo = getObjects(img_clear, 0.45, 0.2, objects=['person'])
    main_frame_checked = False
    # Save detected persons with precision > 50%
    for info in objectInfo: # check if person detected
        box, className, confidence = info
        if className == 'person' and confidence > 0.55:
            print(f"person detected, saving photo in {persons_path}")
            # Save the whole frame with marked persons
            if main_frame_checked is False:
                frame_filename = f'person_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S%f")}_main_frame.jpg'
                cv2.imwrite(os.path.join(persons_path, frame_filename), img_rectangle)
                main_frame_checked = True
            #print(f"Frame saved as {frame_filename}")
            x, y, w, h = box
            # Save the cropped version of the detected person
            person_crop = capture_increase_size(x, y, w, h, img)
            img_time_name = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S%f")) # to sync names of persons and cropped faces
            cv2.imwrite(os.path.join(persons_path, f'person_{img_time_name}.jpg'), person_crop)
            
            # face detection segment
            imgGray = cv2.cvtColor(person_crop,cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(imgGray,1.1,4)
            for (x,y,w,h) in faces:
                image_emotion = person_crop.copy()
                face = person_crop[y:y + h, x:x + w]
                print(f"person face detected, saving photo in {faces_path}")
                cv2.imwrite(os.path.join(faces_path, f'person_{img_time_name}.jpg'), face)
                # Find face emotion
                rgb_frame = cv2.cvtColor(imgGray, cv2.COLOR_GRAY2RGB)
                face_roi = rgb_frame[y:y + h, x:x + w] # roi - region of interest
                face_roi_result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)
                emotion = face_roi_result[0]['dominant_emotion']
                 # Draw rectangle around face and label with predicted emotion
                cv2.rectangle(image_emotion, (x, y), (x + w, y + h), (0, 0, 255), 2)
                 # Calculate the space around the rectangle
                space_top = y  # Space between the face and the top of the image
                space_bottom = person_crop.shape[0] - (y + h)  # Space below the face
                space_left = x  # Space to the left of the face
                space_right = person_crop.shape[1] - (x + w)  # Space to the right of the face
                # Determine which side has the most space
                if space_top >= max(space_bottom, space_left, space_right):
                    # Place text above the face
                    text_position = (x, y - 10)
                elif space_bottom >= max(space_top, space_left, space_right):
                    # Place text below the face
                    text_position = (x, y + h + 30)
                elif space_left >= max(space_top, space_bottom, space_right):
                    # Place text to the left of the face
                    text_position = (x - w - 10, y + h // 2)
                else:
                    # Place text to the right of the face
                    text_position = (x + w + 10, y + h // 2)
                # Draw the text
                cv2.putText(image_emotion, emotion, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                # Save the image with the emotion label
                cv2.imwrite(os.path.join(emotions_path, f'{str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S%f"))}.jpg'), image_emotion)
    cv2.imshow("Output", img_rectangle)
    
    
def check_face(faces_path, persons_path, reference_dir, person_metadata_log_file, face_metadata_log_file):
    reference_img = []
    faces_img = []
    persons_img = []

    with open(person_metadata_log_file, "a+"): # create log files
        pass
    with open(face_metadata_log_file, "a+"): # create log files
        pass
    
    with open(person_metadata_log_file, "r") as person:
        person_metadata_log = person.read().splitlines()
        
    with open(face_metadata_log_file, "r") as face:
        face_metadata_log = face.read().splitlines()

    for root, dirs, files in os.walk(reference_dir): # REFERENCE PHOTOS
        for file in files:
            if file.lower().endswith(".jpg") or file.lower().endswith(".png"):
                img_path = os.path.join(root, file)
                reference_img.append((cv2.imread(img_path), root))  # Save image and its directory
    
    for root, dirs, files in os.walk(faces_path): # FACES
        for file in files:
            if (file.lower().endswith(".jpg") or file.lower().endswith(".png")): # and it's not same photos which checked once
                img_path = os.path.join(root, file)
                if img_path.lower() not in map(str.lower, face_metadata_log):
                    faces_img.append((cv2.imread(img_path), file, root))  # Save image and its directory
    
    for root, dirs, files in os.walk(persons_path): # PERSONS
        for file in files:
            if (file.lower().endswith(".jpg") or file.lower().endswith(".png")): # and it's not same photos which checked once
                img_path = os.path.join(root, file)
                #print(f"person_image_path: {img_path}")
                if img_path.lower() not in map(str.lower, person_metadata_log):
                    persons_img.append((cv2.imread(img_path), file, root))  # Save image and its directory


    with open(person_metadata_log_file, "a") as person:
        for personinfo, filename, person_dir in persons_img:
            path = os.path.join(person_dir, filename)
            person.write(path + "\n")
    with open(face_metadata_log_file, "a") as face:
        for personinfo, filename, face_dir in faces_img:
            path = os.path.join(face_dir, filename)
            face.write(path + "\n")
            
    if not faces_img:
        print("NO FACE DETECTED")
        return
    
    for faceinfo, filename, face_dir in faces_img:
        for reference_image, dir in reference_img:
            try:
                if DeepFace.verify(faceinfo.copy(), reference_image.copy())['verified']:
                    # face_match = True
                    face_path = os.path.join(face_dir, filename) # find face image path
                    for personinfo, target, person_dir in persons_img: # find person image path
                        if filename == target:
                            # rename file
                            name, ext = os.path.splitext(target)
                            person_image = f"{name}_person{ext}"
                            person_path_old = os.path.join(person_dir, target)
                            person_path_new = os.path.join(person_dir, person_image)
                            os.rename(person_path_old, person_path_new)
                            # move files into reference directory
                            if face_path:
                                shutil.move(face_path, dir)
                            if person_path_new:
                                shutil.move(person_path_new, dir)
                    break
                else:
                    continue
            except ValueError:
                pass
    

def video_capture(output_folder, reference_folder, person_metadata_log_file, face_metadata_log_file):
    cap = cv2.VideoCapture(0) # 0 => live stream
    cap.set(3, 640)
    cap.set(4, 480)
    # cap.set(3, 1920)
    # cap.set(4, 1080)
    output_folder += "/video"
    faces_path = f"{output_folder}/faces"
    persons_path = f"{output_folder}/persons"
    emotions_path = f"{output_folder}/emotions"
    if not os.path.exists(faces_path):
        os.makedirs(faces_path)
    if not os.path.exists(persons_path):
        os.makedirs(persons_path)
    if not os.path.exists(emotions_path):
        os.makedirs(emotions_path)
        
    # Timer-related variables
    tick_frequency = cv2.getTickFrequency()  # Get clock frequency
    start_time = cv2.getTickCount()  # Initial start time
    check_next_frames = False
    frames_to_check = 0 # Counter for how many frames are being checked
    seconds_to_wait = 4
    
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to grab frame or finished")
            break
        current_time = cv2.getTickCount()
        time_passed_in_seconds = (current_time - start_time) / tick_frequency
        
        if time_passed_in_seconds >= seconds_to_wait:
            # Start checking for the next 60 frames
            check_next_frames = True
            frames_to_check = 1  # Reset the counter for 60 frames

        if frames_to_check > 0 and check_next_frames:
            # make frame delays ONLY FOR VIDEO CAPTURE
            capture_analyze_save(img, persons_path, faces_path, emotions_path)
            frames_to_check -= 1
        
        if frames_to_check <= 0 and time_passed_in_seconds >= seconds_to_wait:
            check_next_frames = False
            start_time = current_time  # Reset the start time for the next second
            
            # reference segment (call function)
            threading.Thread(target=check_face, args=(faces_path, persons_path, reference_folder, person_metadata_log_file, face_metadata_log_file,)).start()
            #check_face(faces_path, persons_path, reference_folder)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()


# Function to get detected objects and optionally draw on image
def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nms)
    objectInfo = []
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box, className, confidence])
                if draw:
                    cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
                    cv2.putText(img, classNames[classId - 1].upper(), (box[0] + 10, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX,
                                1, (0, 255, 0), 2)
                    cv2.putText(img, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    
    return img, objectInfo

# Main function to process video feed
if __name__ == "__main__":
    # Create a folder to save cropped images if it doesn't exist
    # output_folder = input("input folder path to save content: ")
    # reference_folder = input("input folder path to refer content: ")
    output_folder = 'detected_persons'
    reference_folder = "photos"
    person_metadata_log_file = "person_metadata_log_file.txt" # don't check image again if being checked once
    face_metadata_log_file = "face_metadata_log_file.txt" # don't check image again if being checked once
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(reference_folder):
        os.makedirs(reference_folder)
    
    video_capture(output_folder, reference_folder, person_metadata_log_file, face_metadata_log_file)
    
    cv2.destroyAllWindows()
    

    