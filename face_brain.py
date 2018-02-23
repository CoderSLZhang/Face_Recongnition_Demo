# zhangshulin
# e-mail: zhangslwork@yeah.net
# 2018-2-22


import facenet_adapter
import numpy as np
import scipy


FACE_SIZE = facenet_adapter.FACE_SIZE


class Face_brain:

    def __init__(self):
        self._facenet = facenet_adapter.Facenet()
        self._facenet.build()

    def read_image(self, image_file, mode='RGB'):
        img = scipy.misc.imread(image_file, mode=mode)

        if img.shape != FACE_SIZE:
            img = scipy.misc.imresize(img, FACE_SIZE)

        return np.array([img])

    def read_images(self, image_files, mode='RGB'):
        imgs = []
        for file in image_files:
            img = scipy.misc.imread(file, mode=mode)

            if img.shape != FACE_SIZE:
                img = scipy.misc.imresize(img, FACE_SIZE)

            imgs.append(img)

        return np.array(imgs)

    def encode_faces(self, images):
        if isinstance(images, list):
            images = np.concatenate(images, axis=0)
        return self._facenet.encode_faces(images)

    def compare_faces(self, from_face, to_faces):
        dist = np.sqrt(np.sum(np.square(from_face - to_faces), axis=1))
        return dist

    def recognize_face(self, from_face, to_faces, threshold=0.7):
        return self.compare_faces(from_face, to_faces) < threshold


