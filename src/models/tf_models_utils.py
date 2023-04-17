# model_utils.py
import tensorflow as tf
import pathlib
from keras.models import Sequential
from keras.layers import (
    Dense,
    Dropout,
    Conv2D,
    MaxPooling2D,
    Flatten,
    SimpleRNN,
    LSTM,
    Rescaling,
)
from keras.utils.vis_utils import plot_model
from keras.utils import to_categorical, get_file
import os
import numpy as np
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt


def build_cnn(input_shape, num_classes):
    model = Sequential(
        [
            Rescaling(1.0 / 255),
            Conv2D(32, kernel_size=(3, 3), activation="relu", input_shape=input_shape),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            Conv2D(64, kernel_size=(3, 3), activation="relu"),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            Flatten(),
            Dense(128, activation="relu"),
            Dropout(0.5),
            Dense(num_classes, activation="softmax"),
        ]
    )
    return model


def build_rnn(input_shape, num_classes):
    model = Sequential(
        [
            SimpleRNN(128, activation="relu", input_shape=input_shape),
            Dropout(0.5),
            Dense(num_classes, activation="softmax"),
        ]
    )
    return model


def build_lstm(input_shape, num_classes):
    model = Sequential(
        [
            LSTM(128, activation="relu", input_shape=input_shape),
            Dropout(0.5),
            Dense(num_classes, activation="softmax"),
        ]
    )
    return model


def compile_model(
    model, optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
):
    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)


def train_model(model, x_train, batch_size=32, epochs=10, validation_data=None):
    history = model.fit(
        x_train,
        batch_size=batch_size,
        epochs=epochs,
        validation_data=validation_data,
    )
    return history


def evaluate_model(model, x_test, y_test):
    scores = model.evaluate(x_test, y_test, verbose=0)
    return scores


def viz_model(model, filename):
    path = "viz"
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, filename)
    plot_model(model, to_file=file_path, show_shapes=True, show_layer_names=True)
    print("Model visualization saved to {}".format(filename))


def save_model(model, filename):
    path = "models"
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, filename)
    model.save(file_path)
    print("Model saved to {}".format(filename))


def save_checkpoint(model, filename):
    path = "checkpoints"
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, filename)
    model.save_weights(file_path)
    print("Model checkpoint saved to {}".format(filename))


def plot_performance(history, filename):
    path = "viz"
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, filename)

    plt.plot(history.history["accuracy"])
    plt.plot(history.history["val_accuracy"])
    plt.title("Model Accuracy")
    plt.ylabel("Accuracy")
    plt.xlabel("Epoch")
    plt.legend(["Train", "Validation"], loc="upper left")
    plt.savefig(file_path)
    plt.show()


def mnist_data(input_shape=(28, 28), num_classes=10):
    # Load the MNIST dataset
    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # Reshape the data for the model
    x_train = (
        x_train.reshape(-1, input_shape[0], input_shape[1]).astype("float32") / 255.0
    )
    x_test = (
        x_test.reshape(-1, input_shape[0], input_shape[1]).astype("float32") / 255.0
    )

    # One-hot encode the labels
    y_train = to_categorical(y_train, num_classes)
    y_test = to_categorical(y_test, num_classes)

    return x_train, y_train, x_test, y_test


def img_ds_from_dir(data_dir, img_size=(28, 28), batch_size=32):
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        labels="inferred",
        label_mode="categorical",
        validation_split=0.2,
        image_size=img_size,
        batch_size=batch_size,
        shuffle=True,
        seed=123,
        subset="training",
    )

    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        labels="inferred",
        label_mode="categorical",
        validation_split=0.2,
        image_size=img_size,
        batch_size=batch_size,
        shuffle=True,
        seed=123,
        subset="validation",
    )

    return train_ds, val_ds


def get_flowers_dataset():
    dataset_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"
    archive = tf.keras.utils.get_file(origin=dataset_url, extract=True)
    data_dir = pathlib.Path(archive).with_suffix("")
    print(data_dir)
    return data_dir
