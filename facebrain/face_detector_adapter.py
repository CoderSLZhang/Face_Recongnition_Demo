# zhangshulin
# e-mail: zhangslwork@yeah.net
# 2018-2-23


from facenet.src.align import detect_face
import tensorflow as tf
import numpy as np
from scipy import misc
from skimage import transform


class Face_detector:

    def __init__(self, face_size):
        self._FACE_SIZE = face_size
        self._graph = tf.Graph()
        self._sess = tf.Session(graph=self._graph)


    def __del__(self):
        self._sess.close()


    def build(self):
        with self._graph.as_default():
            self._pnet, self._rnet, self._onet = detect_face.create_mtcnn(
                                                            self._sess, None)

    def detect_faces(self, image, margin=20, min_face_size=20, 
        thresholds=(0.6, 0.7, 0.7), factor=0.709, adjust_face=False, *args, **kw):
        img_size = np.asarray(image.shape)[0:2]

        bounding_boxes, points = detect_face.detect_face( image, min_face_size,
                        self._pnet, self._rnet, self._onet, thresholds, factor)

        bounding_boxes = np.round(bounding_boxes).astype(np.int)
        points = np.round(points).astype(np.int)

        faces = []
        for box in bounding_boxes:
            x0 = np.maximum(box[0] - margin // 2, 0)
            y0 = np.maximum(box[1] - margin // 2, 0)
            x1 = np.minimum(box[2] + margin // 2, img_size[1])
            y1 = np.minimum(box[3] + margin // 2, img_size[0])

            face = image[y0: y1, x0: x1, :]
            resize_face = misc.imresize(face, self._FACE_SIZE, interp='bilinear')
            faces.append(resize_face)

        if len(faces) == 0:
            return None, None, None

        faces = np.stack(faces)

        if adjust_face:
            faces = self._adjust_faces(faces, points, *args, **kw)

        return faces, bounding_boxes, points


    def _adjust_faces(self, faces, points, adjust_angle=10):
        eyes_dist = np.sqrt(np.square(points[0] - points[1]) +
                            np.square(points[5] - points[6]))
        eyes_dist_h = np.abs(points[1] - points[0])
        angles = np.arccos(eyes_dist_h / eyes_dist)

        is_negative_angles = np.squeeze(points[6] < points[5])

        angles = np.where(is_negative_angles, angles * -1, angles)
        angles = angles * (180 / np.pi)

        result_faces = []
        for i in range(len(faces)):
            angle = angles[i]
            face = faces[i]
            if np.abs(angle) <= adjust_angle:
                result_faces.append(face)
                continue

            result_face = transform.rotate(face, angle)
            result_face = np.round(result_face * 255).astype(np.uint8)
            result_faces.append(result_face)

        return np.stack(result_faces) 











