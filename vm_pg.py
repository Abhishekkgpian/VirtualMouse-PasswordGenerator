import cv2
import mediapipe as mp
import pyautogui
import hashlib


def main():
    user_choice = input("Enter your choice (1 for virtual mouse, 2 for password generator): ")

    if user_choice == '1':
        virtualMouse()
    elif user_choice == '2':
        userName = input("Enter your name: ")
        dateOfBirth = input("Enter your date of birth (in xx-xx-xx format): ")
        websiteUrl = input("Enter the website URL: ")
        password = generate_password(userName, dateOfBirth, websiteUrl)
        print("Generated password:", password)
    else:
        print("Invalid choice. Please try again.")






def generate_password(userName, dateOfBirth, websiteUrl):
    # Convert input data to uppercase
    userName = userName.upper()
    dateOfBirth = dateOfBirth.upper()
    websiteUrl = websiteUrl.upper()

    # Concatenate input data
    input_data = userName + dateOfBirth + websiteUrl

    # Compute SHA-256 hash
    sha256 = hashlib.sha256()
    sha256.update(input_data.encode('utf-8'))
    hash_value = sha256.hexdigest()

    # Generate password components
    first_char_value = int(hash_value[:8], 16) % 26  # Scale down to 0-25
    second_char_value = int(hash_value[8:16], 16) % 26  # Scale down to 0-25
    third_char_value = int(hash_value[16:24], 16) % 26  # Scale down to 0-25
    fourth_char_value = int(hash_value[24:32], 16) % 26  # Scale down to 0-25
    numeric_value = sum(int(char, 16) for char in hash_value) % 10000  # Sum of all values

    # Ensure the numeric value is four digits long
    numeric_value_str = str(numeric_value).zfill(4)

    # Generate password using the generated components
    password = chr(ord('A') + first_char_value) + chr(ord('a') + second_char_value) + \
               chr(ord('a') + third_char_value) + chr(ord('a') + fourth_char_value) + \
               '@' + numeric_value_str

    return password


    


def virtualMouse():
    cap = cv2.VideoCapture(0)
    hand_detector = mp.solutions.hands.Hands()
    drawing_utils = mp.solutions.drawing_utils
    screen_width, screen_height = pyautogui.size()
    index_y = 0
    flag=True
    while flag:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = hand_detector.process(rgb_frame)
        hands = output.multi_hand_landmarks
        if hands:
            for hand in hands:
                drawing_utils.draw_landmarks(frame, hand)
                landmarks = hand.landmark
                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x*frame_width)
                    y = int(landmark.y*frame_height)
                    if id == 8:
                        cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                        index_x = screen_width/frame_width*x
                        index_y = screen_height/frame_height*y

                    if id == 4:
                        cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                        thumb_x = screen_width/frame_width*x
                        thumb_y = screen_height/frame_height*y
                        if abs(index_y - thumb_y) < 20:
                            pyautogui.click()
                            pyautogui.sleep(1)
                        elif abs(index_y - thumb_y) < 100:
                            pyautogui.moveTo(index_x, index_y)
                    if id == 20:
                        cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                        little_x = screen_width/frame_width*x
                        little_y = screen_height/frame_height*y
                        if abs(index_y - little_y) < 20:
                            flag=False
                            
        cv2.imshow('Virtual Mouse', frame)
        cv2.waitKey(1)
main()