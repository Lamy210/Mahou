from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import torch
from yolox.models.experimental import attempt_load
from yolox.utils import non_max_suppression, vis

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    mp_hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    model = attempt_load("yolox_s.pth", map_location=torch.device('cpu'))
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        if not success:
            break
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = mp_hands.process(img)
        if results.multi_hand_landmarks:
            landmarks = []
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks.append(hand_landmarks.landmark)
            img_shape = img.shape[:2]
            bboxes = []
            for lms in landmarks:
                bboxes.append(mp.solutions.detection._normalized_to_image_bounding_box([lms], img_shape[0], img_shape[1])[0])
            results = non_max_suppression(model(img, bboxes), conf_thres=0.5, iou_thres=0.5)
            if results[0] is not None:
                class_names = model.class_names
                img = vis(img, results, conf_thres=0.5, class_names=class_names)
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()
    mp_hands.close()

if __name__ == '__main__':
    app.run(debug=True)
