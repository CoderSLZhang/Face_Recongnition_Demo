# zhangshulin
# e-mail: zhangslwork@yeah.net
# 2018-2-22


import tensorflow as tf
import numpy as np
import scipy
from facenet.src.models import inception_resnet_v1


MODEL_CKPT = './face_brain/pretrain_inception_resnet_v1/model-20170512-110547.ckpt'


class Facenet():

    def __init__(self, face_size):
        self._FACE_SIZE = face_size
        self._inputs_op = tf.placeholder(
            dtype=tf.float32,
            shape=(None, face_size[0], face_size[1], 3),
            name='inputs_placeholder')
        embeding_op, _ = inception_resnet_v1.inference(
            self._inputs_op,
            keep_probability=1,
            phase_train=False,
            bottleneck_layer_size=128, weight_decay=0.0, reuse=None)

        self._output_op = tf.nn.l2_normalize(embeding_op, axis=1)

        self._sess = tf.Session()

    def build(self):
        saver = tf.train.Saver()
        saver.restore(self._sess, MODEL_CKPT)

    def encode_faces(self, images):
        resize_images = []
        for image in images:
            if image.shape[:2] != self._FACE_SIZE:
                print('image.shape:', image.shape)
                image = scipy.misc.imresize(image, self._FACE_SIZE, interp='bilinear')
            resize_images.append(image)

        resize_images = np.stack(resize_images)

        preprocess_images = self._prewhiten(resize_images)

        embeding = self._sess.run(
            self._output_op,
            feed_dict={self._inputs_op: preprocess_images})

        return embeding

    def _prewhiten(self, images):
        mean = np.mean(images, axis=(1, 2, 3))
        std = np.std(images, axis=(1, 2, 3))
        std_adj = np.maximum(std, 1.0 / np.sqrt(images[0].size))
        output = (images.T - mean) / std_adj

        return output.T

