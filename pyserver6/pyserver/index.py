import os,sys
from flask import Flask, render_template, request, jsonify
from jinja2 import FileSystemLoader
import base64

#from face_detect import get_facepos

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = './tmp'

@app.route("/", methods=['GET'])
def get_index():
    return render_template('./views/index.html')


import cv2
from concurrent.futures import ProcessPoolExecutor

def camera():
    # VideoCapture オブジェクトを取得します
    capture = cv2.VideoCapture(0)
    while(True):
        ret, frame = capture.read()
        cv2.imshow('frame',frame)
        #cv2.imwrite('./static/Image/camera.jpg',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    capture.release()
    cv2.destroyAllWindows()
    
def web():
    app.run()

if __name__ == '__main__':
    app.debug = True
    with ProcessPoolExecutor() as executor:
        executor.submit(web)
        executor.submit(camera)
    
    