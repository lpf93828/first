import skimage.io
import tensorflow as tf
from tensorflow.python.framework import ops, dtypes
import numpy as np
from matplotlib import pyplot as plt

flags = tf.app.flags
FLAGS = flags.FLAGS

""" minsk.jpg是原始图片文件(338 * 600) """
flags.DEFINE_string('original', 'New_York_night.jpg', 'Original Image')
""" tmp_950_color.jpg是包含某种风格的图片文件(338 * 600) """
flags.DEFINE_string('styled', 'New_York_night_picasso.jpg', 'Styled Image')

""" Tensor占位符，后面用Feed来计算 """
original = tf.placeholder("float", [1, 338, 600, 3])
styled = tf.placeholder("float", [1, 338, 600, 3])

def rgb2yuv(rgb):
    """
    Convert RGB image into YUV https://en.wikipedia.org/wiki/YUV
    """
    rgb2yuv_filter = tf.constant(
        [[[[0.299, -0.169, 0.499],
           [0.587, -0.331, -0.418],
            [0.114, 0.499, -0.0813]]]])
    rgb2yuv_bias = tf.constant([0., 0.5, 0.5])

    temp = tf.nn.conv2d(rgb, rgb2yuv_filter, [1, 1, 1, 1], 'SAME')
    temp = tf.nn.bias_add(temp, rgb2yuv_bias)

    return temp


def yuv2rgb(yuv):
    """
    Convert YUV image into RGB https://en.wikipedia.org/wiki/YUV
    """
    yuv = tf.mul(yuv, 255)
    yuv2rgb_filter = tf.constant(
        [[[[1., 1., 1.],
           [0., -0.34413999, 1.77199996],
            [1.40199995, -0.71414, 0.]]]])
    yuv2rgb_bias = tf.constant([-179.45599365, 135.45983887, -226.81599426])
    temp = tf.nn.conv2d(yuv, yuv2rgb_filter, [1, 1, 1, 1], 'SAME')
    temp = tf.nn.bias_add(temp, yuv2rgb_bias)
    temp = tf.maximum(temp, tf.zeros(temp.get_shape(), dtype=tf.float32))
    temp = tf.minimum(temp, tf.mul(
        tf.ones(temp.get_shape(), dtype=tf.float32), 255))
    temp = tf.div(temp, 255)
    return temp

def concat_images(imga, imgb):
    """
    Combines two color image ndarrays side-by-side.
    """
    ha, wa = imga.shape[:2]
    hb, wb = imgb.shape[:2]
    max_height = np.max([ha, hb])
    total_width = wa + wb
    new_img = np.zeros(shape=(max_height, total_width, 3), dtype=np.float32)
    new_img[:ha, :wa] = imga
    new_img[:hb, wa:wa + wb] = imgb
    return new_img

""" 把含有风格的图像styled转换成yuv格式的灰度图styled_grayscale_yuv """
styled_grayscale = tf.image.rgb_to_grayscale(styled)
styled_grayscale_rgb = tf.image.grayscale_to_rgb(styled_grayscale)
styled_grayscale_yuv = rgb2yuv(styled_grayscale_rgb)

""" 把需要添加风格的原始图像转换成yuv格式original_yuv """
original_yuv = rgb2yuv(original)

""" 
组合图像：
1. styled_grayscale_yuv的Y分量
2. original_yuv的U分量
3. original_yuv的V分量
"""
combined_yuv = tf.concat(3, [tf.split(3, 3, styled_grayscale_yuv)[0], tf.split(3, 3, original_yuv)[1], tf.split(3, 3, original_yuv)[2]])

""" 转换成RGB格式 """
combined_rbg = yuv2rgb(combined_yuv)

""" 初始化 """
init = tf.initialize_all_variables()

with tf.Session() as sess:
    sess.run(tf.initialize_all_variables())

    """ 读取需要添加风格的原始图片 """
    original_image = skimage.io.imread(FLAGS.original) / 255.0
    original_image = original_image.reshape((1, 338, 600, 3))

    """ 读取含有风格的图片 """
    styled_image = skimage.io.imread(FLAGS.styled) / 255.0
    styled_image = styled_image.reshape((1, 338, 600, 3))

    """ 为原始图片添加上风格 """
    combined_rbg_ = sess.run(combined_rbg, feed_dict={original: original_image, styled: styled_image})

    """ 拼接几幅图片并保存，做个对比 """
    summary_image = concat_images(original_image.reshape((338, 600, 3)), styled_image.reshape((338, 600, 3)))
    summary_image = concat_images(summary_image, combined_rbg_[0])
    plt.imsave("results.jpg", summary_image)