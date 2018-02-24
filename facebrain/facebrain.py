# zhangshulin
# e-mail: zhangslwork@yeah.net
# 2018-2-22


from facebrain import facenet_adapter
from facebrain import face_detector_adapter
import numpy as np
import scipy


class Facebrain:

    def __init__(self, face_size=(150, 150)):
        self._FACE_SIZE = face_size
        self._facenet = facenet_adapter.Facenet(face_size=face_size)
        self._facenet.build()

    def read_image(self, image_file, mode='RGB'):
        img = scipy.misc.imread(image_file, mode=mode)
        return np.array([img])

    def read_images(self, image_files, mode='RGB'):
        imgs = []
        for file in image_files:
            img = scipy.misc.imread(file, mode=mode)
            imgs.append(img)

        return np.array(imgs)

    def encode_faces(self, images):
        if isinstance(images, list):
            images = np.stack(images)
        return self._facenet.encode_faces(images)

    def compare_faces(self, from_face, to_faces):
        dist = np.sqrt(np.sum(np.square(from_face - to_faces), axis=1))
        return dist

    def recognize_face(self, from_face, to_faces, threshold=0.7):
        return self.compare_faces(from_face, to_faces) < threshold

    def detect_faces(self, image):
        return face_detector_adapter.face_detect(image[0], self._FACE_SIZE)

