import cv2
import json
import numpy as np
from io import BytesIO
from flask import Flask, request, Response
import mediapipe as mp

app = Flask(__name__)

# メディアパイプの設定
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# カメラの設定
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# YOLOXの設定
# ...

@app.route('/process_image', methods=['GET'])
def process_image():
    # 映像を取得
    ret, frame = cap.read()

    # 映像をYOLOXで処理
    # ...

    # 映像をMediapipeで処理
    with mp_pose.Pose(
        static_image_mode=False, min_detection_confidence=0.5) as pose:
        # Convert the image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image using Mediapipe
        results = pose.process(image)

        # Convert the results to JSON
        json_results = json.dumps(results.to_dict())

        # Visualize the results
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # JSON形式で結果を返す
    return Response(json_results, mimetype='application/json')

@app.route('/')
def index():
    return '''
        <html>
            <head>
                <title>Webcam Test</title>
            </head>
            <body>
                <h1>Webcam Test</h1>
                <img src="/video_feed">
            </body>
        </html>
    '''

def gen():
    while True:
        ret, frame = cap.read()
        

        # 映像をYOLOXで処理
        # ...

        # 映像をMediapipeで処理
        with mp_pose.Pose(
            static_image_mode=False, min_detection_confidence=0.5) as pose:
            # Convert the image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the image using Mediapipe
            results = pose.process(image)

            # Visualize the results
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            results = pose.process(image)

            # Visualize the results
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Convert the image to bytes and stream it to the client
            img_bytes = cv2.imencode('.jpg', image)[1].tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
