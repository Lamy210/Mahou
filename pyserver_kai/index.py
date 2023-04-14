import os
from flask import Flask, render_template, request, jsonify
from jinja2 import FileSystemLoader
from flask_caching import Cache


app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = './tmp'

# 静的ファイルの読み込み
app.static_folder = 'static'

# テンプレートファイルの場所とテンプレートエンジンの設定
template_loader = FileSystemLoader(searchpath='./templates')
app.jinja_loader = template_loader

@app.route("/", methods=['GET'])
@cache.cached(timeout=10)
def get_index():
    return render_template('index.html')

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
    # Flask の起動方法を変更
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
