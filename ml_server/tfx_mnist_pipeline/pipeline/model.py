import tensorflow as tf
from tensorflow import keras
from tfx.utils import path_utils

def run_fn(fn_args):
    # Load data from tfrecord files
    def _input_fn(file_pattern, batch_size):
        dataset = tf.data.TFRecordDataset(filenames=[file_pattern])
        # Parse the record into tensors
        def _parse_function(record):
            features = {
                'image': tf.io.FixedLenFeature([], tf.string),
                'label': tf.io.FixedLenFeature([], tf.int64),
            }
            parsed = tf.io.parse_single_example(record, features)
            image = tf.io.decode_raw(parsed['image'], tf.uint8)
            image = tf.cast(image, tf.float32) / 255.0
            image = tf.reshape(image, [28, 28])
            label = tf.cast(parsed['label'], tf.int32)
            return image, label
        dataset = dataset.map(_parse_function)
        dataset = dataset.shuffle(buffer_size=1000).batch(batch_size)
        return dataset

    train_dataset = _input_fn(fn_args.train_files[0], batch_size=64)
    eval_dataset = _input_fn(fn_args.eval_files[0], batch_size=64)

    # Build the model
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(10, activation='softmax'),
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'],
    )

    # Train the model
    model.fit(
        train_dataset,
        validation_data=eval_dataset,
        epochs=5,
    )

    # Save the model
    model.save(fn_args.serving_model_dir, save_format='tf')
