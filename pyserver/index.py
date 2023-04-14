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

'''
@app.route("/api", methods=['POST'])
def face_detect():
    img = request.files['image']
    name = img.filename
    path = os.path.join(app.config['UPLOAD_FOLDER'], name)
    img.save(path)
    face_pos = get_facepos(path)
    return jsonify(face_pos)
'''

if __name__ == '__main__':
    app.debug = True
    app.run()