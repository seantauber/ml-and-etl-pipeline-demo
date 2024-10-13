import tensorflow as tf
import os

def write_tfrecords(data, labels, filename):
    with tf.io.TFRecordWriter(filename) as writer:
        for image, label in zip(data, labels):
            features = {
                'image': tf.train.Feature(bytes_list=tf.train.BytesList(value=[image.tobytes()])),
                'label': tf.train.Feature(int64_list=tf.train.Int64List(value=[label])),
            }
            example = tf.train.Example(features=tf.train.Features(feature=features))
            writer.write(example.SerializeToString())

def main():
    (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()
    os.makedirs('data', exist_ok=True)
    write_tfrecords(train_images, train_labels, 'data/train.tfrecord')
    write_tfrecords(test_images, test_labels, 'data/eval.tfrecord')

if __name__ == '__main__':
    main()
