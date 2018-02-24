# zhangshulin
# e-mail: zhangslwork@yeah.net
# 2018-2-23


from facenet.src.align import detect_face
import tensorflow as tf
import numpy as np
from scipy import misc


def face_detect(image, face_size, margin=10):
    minsize = 20  # minimum size of face
    threshold = [0.6, 0.7, 0.7]  # three steps's threshold
    factor = 0.709  # scale factor

    img_size = np.asarray(image.shape)[0:2]

    with tf.Graph().as_default():
        with tf.Session() as sess:
            pnet, rnet, onet = detect_face.create_mtcnn(sess, None)

            bounding_boxes, _ = detect_face.detect_face(
                image, minsize, pnet, rnet, onet, threshold, factor)

    bounding_boxes = bounding_boxes.astype(np.int)

    faces = []
    for box in bounding_boxes:
        x0 = np.maximum(box[0] - margin // 2, 0)
        y0 = np.maximum(box[1] - margin // 2, 0)
        x1 = np.minimum(box[2] + margin // 2, img_size[1])
        y1 = np.minimum(box[3] + margin // 2, img_size[0])

        face = image[y0: y1, x0: x1, :]
        resize_face = misc.imresize(face, face_size, interp='bilinear')
        faces.append(resize_face)

    if len(faces) == 0:
        return None, None

    return np.stack(faces), bounding_boxes

