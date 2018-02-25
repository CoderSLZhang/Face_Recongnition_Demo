# zhangshulin
# e-mail: zhangslwork@yeah.net
# 2018-2-24


import sys
import os
os.chdir('../')
sys.path.append('./')

from facebrain.facebrain import Facebrain
from flask import Flask, request, Response
import json
import os
import scipy 


FACES_DIR = './demo/faces_database'


if not os.path.exists(FACES_DIR):
    os.mkdir(FACES_DIR)

facebrain = Facebrain()

app = Flask(__name__)


@app.route('/upload_face', methods=['POST'])
def upload_face():
    file = request.files['file']
    img = facebrain.read_image(file)
    faces, _ , __ = facebrain.detect_faces(img, adjust_face=True)

    if faces is None:
        return_json = json.dumps({
            'error': '无法检测到人脸',
            'message': None})

        return Response(return_json, mimetype='text/json')

    name = request.form.get('name')
    scipy.misc.imsave(os.path.join(FACES_DIR, name + '.png'), faces[0])

    return_json = json.dumps({
        'error': None,
        'message': '人脸采集成功'})

    return Response(return_json, mimetype='text/json')


@app.route('/recognize_face', methods=['POST'])
def recognize_face():
    file = request.files['file']
    img = facebrain.read_image(file)
    faces, _, __ = facebrain.detect_faces(img, adjust_face=True)

    if faces is None:
        return_json = json.dumps({
            'error': '无法检测到人脸',
            'message': None})

        return Response(return_json, mimetype='text/json')

    face_paths = []
    names = []
    for file in os.listdir(FACES_DIR):
        path = os.path.join(FACES_DIR, file)
        name, ext = os.path.splitext(file)
        if ext != '.png':
            continue

        face_paths.append(path)
        names.append(name)

    upload_encoding = facebrain.encode_faces(faces[0])
    database_faces = facebrain.read_images(face_paths)
    database_encodings = facebrain.encode_faces(database_faces)

    compare_result = facebrain.recognize_face(upload_encoding, database_encodings)

    try:
        right_index = list(compare_result).index(True)
        name = names[right_index]
    except ValueError:
        name = 'unknown'

    return_json = json.dumps({'error': None, 'message': name})

    return Response(return_json, mimetype='text/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8800)

