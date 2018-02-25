# zhangshulin
# e-mail: zhangslwork@yeah.net
# 2018-2-22


from facebrain.facenet_adapter import Facenet
from facebrain.face_detector_adapter import Face_detector
import numpy as np
import scipy


class Facebrain:

    def __init__(self, face_size=(150, 150)):
        self._facenet = Facenet(face_size=face_size)
        self._face_detector = Face_detector(face_size=face_size)
        self._facenet.build()
        self._face_detector.build()


    def read_image(self, image_file, mode='RGB'):
        img = scipy.misc.imread(image_file, mode=mode)
        return np.array([img])


    def read_images(self, image_files, mode='RGB'):
        imgs = []
        for file in image_files:
            img = scipy.misc.imread(file, mode=mode)
            imgs.append(img)

        return np.array(imgs)


    def detect_faces(self, image, *args, **kw):
        return self._face_detector.detect_faces(image[0], *args, **kw)


    def encode_faces(self, images):
        if isinstance(images, list):
            images = np.stack(images)
        elif images.ndim == 3:
            images = np.expand_dims(images, axis=0)

        return self._facenet.encode_faces(images)


    def compare_faces(self, from_face, to_faces):
        if from_face.ndim == 1:
            from_face = np.expand_dims(from_face, axis=0)

        if to_faces.ndim == 1:
            to_faces = np.expand_dims(to_faces, axis=0)

        dist = np.sqrt(np.sum(np.square(from_face - to_faces), axis=1))
        return dist


    def recognize_face(self, from_face, to_faces, threshold=0.68):
        return self.compare_faces(from_face, to_faces) < threshold

    

