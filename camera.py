import cv2
from detection import AccidentDetectionModel
import numpy as np
import os
import winsound
import threading
import time
import tkinter as tk
from twilio.rest import Client
from PIL import Image, ImageTk

# Load your model
model = AccidentDetectionModel("model.json", "model_weights.keras")
font = cv2.FONT_HERSHEY_SIMPLEX
alarm_triggered = False

def save_accident_photo(frame):
    try:
        current_date_time = time.strftime("%Y-%m-%d-%H%M%S")
        directory = "accident_photos"
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = f"{directory}/{current_date_time}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Accident photo saved as {filename}")
    except Exception as e:
        print(f"Error saving accident photo: {e}")

def call_ambulance():
    try:
        account_sid = 'ACc79198e9bb1be5881aab78a6c2d0e8d2'
        auth_token = '80a7bf4296a33137567f6b8f3bc85900'
        client = Client(account_sid, auth_token)
        call = client.calls.create(
            url='https://redwood-leopard-4168.twil.io/call',
            to='+918217464429',
            from_='+15087153683'
        )
        print(call.sid)
    except Exception as e:
        print(f"Error calling ambulance: {e}")

def send_sms_alert():
    try:
        account_sid = 'ACc79198e9bb1be5881aab78a6c2d0e8d2'
        auth_token = '80a7bf4296a33137567f6b8f3bc85900'
        client = Client(account_sid, auth_token)

        latitude = 12.990252
        longitude = 76.113450
        maps_link = f"https://maps.app.goo.gl/n8FxMpyVd7tXzfSn8?g_st=aw={latitude},{longitude}"
        body = f"\n !!!! Emergency Alert: Accident Detected at \nLocation: {maps_link}. \nPlease take necessary action. !!!!"

        message = client.messages.create(
            body=body,
            from_='+15087153683',
            to='+918217464429'
        )
        print(f"Message SID: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

def get_latest_accident_photo():
    directory = "accident_photos"
    try:
        files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".jpg")]
        if not files:
            print("No accident photos found!")
            return None
        latest_file = max(files, key=os.path.getctime)
        return latest_file
    except Exception as e:
        print(f"Error fetching latest accident photo: {e}")
        return None

def show_alert_message():
    def on_call_ambulance():
        send_sms_alert()
        call_ambulance()
        alert_window.destroy()

    frequency = 2500
    duration = 2000
    winsound.Beep(frequency, duration)

    alert_window = tk.Tk()
    alert_window.title("Alert")
    alert_window.geometry("700x500")

    alert_label = tk.Label(alert_window, text="Alert: Accident Detected!\n\nIs the Accident Critical?", fg="black", font=("Helvetica", 16))
    alert_label.pack()

    latest_photo_path = get_latest_accident_photo()
    if latest_photo_path:
        try:
            gif = Image.open(latest_photo_path)
            resized_gif = gif.resize((450, 350), Image.BICUBIC)
            global gif_image
            gif_image = ImageTk.PhotoImage(resized_gif)
            gif_label = tk.Label(alert_window, image=gif_image)
            gif_label.pack()
        except Exception as e:
            print(f"Error loading image: {e}")
    else:
        print("No accident image available to display.")

    call_ambulance_button = tk.Button(alert_window, text="Call Ambulance", command=on_call_ambulance)
    call_ambulance_button.pack()

    cancel_button = tk.Button(alert_window, text="Cancel", command=alert_window.destroy)
    cancel_button.pack()

    alert_window.mainloop()

def start_alert_thread():
    alert_thread = threading.Thread(target=show_alert_message)
    alert_thread.daemon = True
    alert_thread.start()

def startapplication():
    global alarm_triggered

    video = cv2.VideoCapture(0)  # ✅ LIVE CAMERA

    if not video.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = video.read()
        if not ret:
            print("Failed to grab frame")
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        roi = cv2.resize(gray_frame, (250, 250))

        pred, prob = model.predict_accident(roi[np.newaxis, :, :])
        if pred == "Accident" and not alarm_triggered:
            prob = round(prob[0][0] * 100, 2)
            if prob > 99:
                save_accident_photo(frame)
                alarm_triggered = True
                start_alert_thread()

        cv2.rectangle(frame, (0, 0), (280, 40), (0, 0, 0), -1)
        cv2.putText(frame, pred + " " + str(prob), (20, 30), font, 1, (255, 255, 0), 2)

        frame = cv2.resize(frame, (1280, 720))
        cv2.imshow('Live Accident Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    startapplication()
