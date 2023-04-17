from keras.models import load_model
from keras.utils import load_img, img_to_array
from numpy import argmax


# load and prepare the image
def load_image(filename, target_size=(28, 28)):
    target_size = (28, 28)
    img = load_img(filename, grayscale=True, target_size=target_size)
    wd, ht = target_size
    img = img_to_array(img)
    # reshape into a single sample with 1 channel
    img = img.reshape(1, wd, ht, 1)
    # prepare pixel data
    img = img.astype("float32")
    img = img / 255.0
    return img


# load an image and predict the class
def predict_image(model, filename, target_size=(28, 28)):
    img = load_image(filename, target_size=target_size)
    predict_digit = model.predict(img)
    prediction = argmax(predict_digit)
    return prediction


# usage
model = load_model("models/model.h5")

digit = predict_image(model, "data/external/7.png")
print(digit)
