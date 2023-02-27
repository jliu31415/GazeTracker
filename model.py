import numpy as np
from tensorflow import keras
from keras import layers
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

  # load csv data (contains labels)
  # positions of eye unused; assume face in center of screen
  with open(folder + "data.csv", "r") as f:
      csv_data = np.array(list(csv.reader(f, delimiter=",")))
  labels = csv_data[:, -1].astype(np.uint8)
  print(labels[0])
  # encode the labels as one-hot vectors
  one_hot = lambda x: np.array([x==0, x==1, x==2, x==3])
  labels = np.array(list(map(one_hot, labels)))
  
  # create cnn
  inputs = keras.Input(shape=image_shape)
  x = layers.Rescaling(1.0/255)(inputs)
  for filters in 8, 16:
    x = layers.Conv2D(filters, (3, 3), activation="relu", padding="same")(x)
    x = layers.MaxPooling2D(pool_size=(2, 2))(x)
    x = layers.Dropout(0.25)(x)
  x = layers.Flatten()(x)
  x = layers.Dense(16, activation="relu")(x)
  x = layers.Dropout(0.5)(x)
  x = layers.Dense(4, activation="softmax")(x)
  model = keras.Model(inputs, x)

  # compile cnn
  model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
  # es = keras.callbacks.EarlyStopping(monitor="accuracy", patience=3, verbose=1)
  model.fit(training_images, labels, epochs=32, batch_size=32)
  return model

# model = train_model()
# model.save("model_v1")

model = keras.models.load_model("saved_model_v1")
# ignore csv data; only use training image as input
def predict(training_image, csv_row):
  training_image = np.array([training_image])
  return model.predict(training_image)