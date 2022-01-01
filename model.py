import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras import callbacks
import os
import cv2
import csv

def train_model():
  # load images
  folder = "saved_dataset/"
  image_shape = (50, 100, 1)
  training_images = np.empty((0,) + image_shape).astype(np.uint8)
  file_names = np.empty(0)

  for file in os.listdir(folder + "frames/"):
      file_names = np.append(file_names, file)
      image = cv2.imread(folder + "frames/" + file, 0).reshape(*image_shape)
      training_images = np.append(training_images, [image], axis=0)

  # load csv data
  with open(folder + "data.csv", "r") as f:
      csv_data = np.array(list(csv.reader(f, delimiter=",")))
  labels = csv_data[:, -1].astype(int)
  csv_data = csv_data[:, :-2].astype(int)
  
  # create cnn
  inputs = keras.Input(shape=image_shape)
  x = layers.Rescaling(1.0/255)(inputs)
  for filters in 16, 32, 64:
    x = layers.Conv2D(filters, (3, 3), activation="relu", padding="same")(x)
    x = layers.BatchNormalization(axis=-1)(x)
    x = layers.MaxPooling2D(pool_size=(2, 2))(x)
  x = layers.Flatten()(x)
  x = layers.Dense(16, activation="relu")(x)
  x = layers.BatchNormalization(axis=-1)(x)
  x = layers.Dropout(0.5)(x)
  x = layers.Dense(8, activation="relu")(x)
  cnn = keras.Model(inputs, x)

  # create mlp
  mlp = keras.Sequential()
  mlp.add(layers.Dense(32, input_dim=np.size(csv_data[0]), activation="relu"))
  mlp.add(layers.Dense(16, activation="relu"))
  mlp.add(layers.Dense(8, activation="relu"))

  # create the input to our final set of layers as the *output* of both the CNN and MLP
  combinedInput = layers.concatenate([cnn.output, mlp.output])
  x = layers.Dense(32, activation="relu")(combinedInput)
  x = layers.Dense(16, activation="relu")(x)
  x = layers.Dense(8, activation="softmax")(x)
  model = keras.Model(inputs=[cnn.input, mlp.input], outputs=x)

  # compile and train
  model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
  es = callbacks.EarlyStopping(monitor="accuracy", patience=3, verbose=1)
  model.fit([training_images, csv_data], labels, epochs=32, batch_size=32, callbacks=es)
  return model

# model = train_model()
# model.save("saved_model_v2")

model = keras.models.load_model("saved_model_v2")
def predict(training_image, csv_row):
  training_image = np.array([training_image])
  csv_row = np.array([csv_row])
  return model.predict((training_image, csv_row))