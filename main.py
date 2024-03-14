import pyttsx3
from decouple import config
from datetime import datetime

import mediapipe as mp
import time
import speech_recognition as sr
import llama2
from functions.os_ops import open_calculator, open_camera, open_cmd, open_notepad
from functions.online_ops import play_on_youtube, search_on_google, find_my_ip
import webbrowser
import os
import wikipedia
import pywhatkit as kit

import cv2
import dlib
import numpy as np
import pyautogui


def eye_mouse_control():
    # Load the pre-trained facial landmark detector model
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_face_landmarks.dat")

    # Get the screen resolution
    screen_width, screen_height = pyautogui.size()

    # Open a video capture device (webcam)
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = detector(gray)

        for face in faces:
            # Detect facial landmarks
            landmarks = predictor(gray, face)

            # Get the position of the left and right eyes
            left_eye_pos = (landmarks.part(36).x, landmarks.part(36).y)
            right_eye_pos = (landmarks.part(45).x, landmarks.part(45).y)

            # Calculate the midpoint between the eyes
            midpoint = ((left_eye_pos[0] + right_eye_pos[0]) // 2, (left_eye_pos[1] + right_eye_pos[1]) // 2)

            # Move the mouse cursor based on the midpoint position
            x, y = midpoint
            x = np.interp(x, [0, screen_width], [0, screen_width])
            y = np.interp(y, [0, screen_height], [0, screen_height])
            pyautogui.moveTo(x, y)

        # Display the frame
        cv2.imshow("Eye Mouse Control", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture device and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    eye_mouse_control()

# from openai import OpenAI, ChatCompletion, chat
# import bardapi
# from bardapi import core, Bard

USERNAME = config('USER')
BOT = config('BOT')

# mp_drawing = mp.solutions.drawing_utils
# mp_hands = mp.solutions.hands
#
#
# # Define gesture recognition function
# def detect_gesture(hand_landmarks):
#     # Your gesture detection logic here
#     # For example, you can detect swipe gestures based on the position of landmarks
#     # Return the detected gesture
#     pass


# Main code
# def jarvis_with_gesture():
#     mp_hands_module = mp_hands.Hands(
#         max_num_hands=1,
#         model_complexity=0,
#         min_detection_confidence=0.3,
#         min_tracking_confidence=0.3
#     )
#
#     cam = cv2.VideoCapture(0)
#     wcam, hcam = 640, 480
#     cam.set(3, wcam)
#     cam.set(4, hcam)
#
#     while cam.isOpened():
#         success, image = cam.read()
#         if not success:
#             break
#         image = cv2.flip(image, 1)
#
#         # Process the image
#         image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         result = mp_hands_module.process(image_rgb)
#
#         # Gesture recognition
#         if results.multi_hand_landmarks:
#             for hand_landmarks in results.multi_hand_landmarks:
#                 # Detect gesture
#                 detect_gesture(hand_landmarks)
#
#                 # Perform action based on gesture
#                 if gesture == "swipe_left":
#                     # Do something
#                     pass
#                 elif gesture == "swipe_right":
#                     # Do something else
#                     pass
#                 # Add more conditions for other gestures
#
#                 # Draw hand landmarks
#                 mp_drawing.draw_landmarks(
#                     image,
#                     hand_landmarks,
#                     mp_hands.HAND_CONNECTIONS,
#                     mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
#                     mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
#                 )
#
#         # Display the image
#         cv2.imshow("Hand Gesture Recognition", image)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     # Release the camera and close OpenCV windows
#     cam.release()
#     cv2.destroyAllWindows()
#
#
# if __name__ == "__main__":
#     jarvis_with_gesture()

engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 190)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

contacts = {
    'dad': '9426331934',
    'mum': '9426756926',
    'sis': '9426397934',
    'dada': '9427388632'
    # Add more contacts as needed
}


def send_whatsapp_message(numbers, messages):
    kit.sendwhatmsg_instantly(f"+91{numbers}", messages)

    # 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   api key
    # AIzaSyA32IcZsxzltNq-Be8B_4QpNuYBKK_VUEU   Google Bard

    # def ai():
    #     # Initialize OpenAI client
    #     OPENAI_API_KEY = "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"
    #     client = OpenAI(api_key=OPENAI_API_KEY)
    #     speak("what u want to know sir!")

    try:
        user_message = {
            "role": "user",
            "content": take_user_input(),

        }
        print(user_message)
        # Generate a response using chat completion
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[user_message],
        )

        response = chat_completion.choices[0].message.content
        print(response)
    except Exception as e:
        print(f"Error: {e}")
        speak("Sorry Sir, Can't Do It")


def speak(text):
    engine.say(text)
    engine.runAndWait()


def greet_user():
    hour = datetime.now().hour

    if 6 <= hour < 12:
        speak(f"Good Morning {USERNAME}")
    elif 12 <= hour < 16:
        speak(f"Good Afternoon {USERNAME}!")
    elif 16 <= hour < 19:
        speak(f"Good Evening! {USERNAME}")
    else:
        speak(f"Good Night!{USERNAME}")

    speak(f"I am {BOT} how may i help you")


def open_website(url):
    webbrowser.open(url)


def search_on_wikipedia(queries):
    result = wikipedia.summary(queries, sentences=2)
    return result


def open_time():
    current_time = datetime.now().strftime("%H:%M")
    current_date = datetime.now().strftime("%Y-%m-%d")

    speak(f"The current time is {current_time} and the date is {current_date}.")


def take_user_input():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Adjusting noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Recording for 4 seconds...")
            recorded_audio = recognizer.listen(source, timeout=3)
            print("Done recording.")
        try:
            queries = recognizer.recognize_google(recorded_audio, language="en-IN").lower()
            print(f": Said {queries}")
            return queries

        except:
            print(speak("You Failed Try Again"))

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
    except Exception as ex:
        print("Error during recognition:", ex)


if __name__ == '__main__':
    greet_user()
    while True:
        query = take_user_input()

        if query is not None:
            if 'open website' in query:
                open_website("https://web.whatsapp.com/")
                speak("is there anything else i can do for u sir?")

            elif "hello" in query:
                speak(f"Hello  How are you, am i working properly?")

            elif 'time' in query:
                open_time()

            elif "open notepad" in query:
                open_notepad()

            elif 'open command prompt' in query or 'open cmd' in query:
                open_cmd()

            elif 'open camera' in query:
                open_camera()

            elif 'open calculator' in query:
                open_calculator()

            elif 'ip address' in query:
                ip_address = find_my_ip()
                speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
                print(f'Your IP Address is {ip_address}')

            elif "wikipedia" in query:
                speak('What information do you want, sir?')
                search_query = take_user_input()
                if search_query is not None:
                    results = search_on_wikipedia(search_query)
                    speak(f"According to Wikipedia, {results}")
                    speak("For your convenience, I am printing it on the screen sir.")
                    print(results)

            elif "youtube" in query:
                speak('What do you want to play on Youtube, sir?')
                video = take_user_input()
                if video is not None:
                    play_on_youtube(video)

            elif "google" in query:
                speak('What do you want to search on Google, sir?')
                search_query = take_user_input()
                if search_query is not None:
                    search_on_google(search_query)

            elif "send whatsapp message" in query:
                speak('whom do you want to send message sir? ')
                name = take_user_input()
                if name in contacts:
                    number = contacts.get(name)
                    speak("What is the message sir?")
                    message = take_user_input()
                    if message is not None:
                        send_whatsapp_message(number, message)
                        speak("I've sent the message sir.")

            elif "open music" in query:
                musicPath = "C:\\Users\\manav\\Downloads\\Ram-Siya-Ram-(Hindi)(PaglaSongs).mp3"
                os.startfile(musicPath)

            elif "riyal" in query:
                speak("i know sir Ria son is your sister, & dont mind but she is pretty but also fat and cute")

            # elif "ai" in query:
            #     ai()

            # elif "jarvis" in query:
            #     speak("one second sir..")
            #     bard_ai()

            elif "remember that" in query:
                rememberMsg = query.replace("jarvis", "")
                rememberMsg = rememberMsg.replace("remember that", "")
                speak("You told me to remember:" + rememberMsg)
                remeber = open("D:\\Mana\\JARVIS\\remeber.txt", 'w')
                remeber.write(rememberMsg)
                remeber.close()

            elif "do you remember something" in query:
                remeber = open("D:\\Mana\\JARVIS\\remember.txt", 'r')
                speak("Yes sir you told me to remember that:" + remeber.read())

            elif "exit" in query:
                speak("Okay Good Bye Sir Meet You Soon")
                exit()
