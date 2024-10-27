# -*- coding: utf-8 -*-
"""Copy of fcc_cat_dog.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1egBGW071sAimpp0DD0PbjY-JcP1E_AQY
"""

# Commented out IPython magic to ensure Python compatibility.
# import required libraries

try:
  # This command only in Colab.
#   %tensorflow_version 2.x
except Exception:
  pass
import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D, Input
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import os
import numpy as np
import matplotlib.pyplot as plt

# Download data and sets key variables

# Get project files
!wget https://cdn.freecodecamp.org/project-data/cats-and-dogs/cats_and_dogs.zip

!unzip cats_and_dogs.zip

# sets path to file
PATH = 'cats_and_dogs'

# create directories for each set of data
train_dir = os.path.join(PATH, 'train')
validation_dir = os.path.join(PATH, 'validation')
test_dir = os.path.join(PATH, 'test')

# Get number of files in each directory. The train and validation directories
# each have the subdirecories "dogs" and "cats".
total_train = sum([len(files) for r, d, files in os.walk(train_dir)])
total_val = sum([len(files) for r, d, files in os.walk(validation_dir)])
total_test = len(os.listdir(test_dir))

# Variables for pre-processing and training.
batch_size = 128
epochs = 15 # number of epochs, change to higher num to get better accuracy
IMG_HEIGHT = 150
IMG_WIDTH = 150

# 3

# Use image generator to read/decode images and convert to floating point tensors
train_image_generator = ImageDataGenerator(rescale=1./255)
validation_image_generator = ImageDataGenerator(rescale=1./255)
test_image_generator = ImageDataGenerator(rescale=1./255)

# Use flow_from_directory to load, rescale and resize images
train_data_gen = train_image_generator.flow_from_directory(
    batch_size=batch_size, 
    directory=train_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    class_mode='binary')
val_data_gen = train_image_generator.flow_from_directory(
    batch_size=batch_size,
    directory=validation_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    class_mode='binary')
test_data_gen = train_image_generator.flow_from_directory(
    batch_size=batch_size,
    directory= test_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    shuffle=False,
    classes=['.']) # class already in test_dir

# 4

# Takes array of images and probabilites list(probabilities list is optional)
# Plots five random training images
def plotImages(images_arr, probabilities = False):
    fig, axes = plt.subplots(len(images_arr), 1, figsize=(5,len(images_arr) * 3))
    if probabilities is False:
      for img, ax in zip( images_arr, axes):
          ax.imshow(img)
          ax.axis('off')
    else:
      for img, probability, ax in zip( images_arr, probabilities, axes):
          ax.imshow(img)
          ax.axis('off')
          if probability > 0.5:
              ax.set_title("%.2f" % (probability*100) + "% dog")
          else:
              ax.set_title("%.2f" % ((1-probability)*100) + "% cat")
    plt.show()

sample_training_images, _ = next(train_data_gen)
plotImages(sample_training_images[:5])

# 5

# With the small number of training data, we have to account for overfitting
# We can create more training data from existing data through random transformations

# Image augmentation: put image through few random transformations
train_image_generator = ImageDataGenerator(
                                rescale=1./255,
                                rotation_range=45,
                                width_shift_range=.2,
                                height_shift_range=.2,
                                horizontal_flip=True,
                                vertical_flip=True,
                                zoom_range=0.2)

# 6

# Create train_data_gen again, with the new train_image_generator
train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                     directory=train_dir,
                                                     target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                     class_mode='binary')

# Single image is plotted 5 times, with various transformations
augmented_images = [train_data_gen[0][0][0] for i in range(5)]

plotImages(augmented_images)

# 7

# Create neural network that outputs class probabilities
model = Sequential([
    Conv2D(32, 3, padding='same', activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH ,3)),
    MaxPooling2D(2),
    Conv2D(64, 3, padding='same', activation='relu'),
    MaxPooling2D(2),
    Conv2D(128, 3, padding='same', activation='relu'),
    MaxPooling2D(2),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(2)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy']) # compile model and view training/validation accuracy for training epoch

model.summary()

# 8

# Train the model using fit()
history = model.fit(
    x=train_data_gen,
    steps_per_epoch=total_train // batch_size,
    epochs=epochs,
    validation_data=val_data_gen,
    validation_steps=total_val // batch_size
)

# 9

# Visualize the accuracy and loss of the model
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

# 10

# Use model to predict cat or dog
probabilities = np.argmax(model.predict(test_data_gen), axis=-1) # get index of max value, using last axis
sample_testing_images, _ = next(test_data_gen) # generate testing images using test_data_gen
plotImages(sample_training_images[:50], probabilities) # print out last 50 images alongside probabilities

# 11
answers =  [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0,
            1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0,
            1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1,
            1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 
            0, 0, 0, 0, 0, 0]

correct = 0

for probability, answer in zip(probabilities, answers):
  if np.round(probability) == answer:
    correct +=1

percentage_identified = (correct / len(answers)) * 100

passed_challenge = percentage_identified >= 63

print(f"Your model correctly identified {round(percentage_identified, 2)}% of the images of cats and dogs.")

if passed_challenge:
  print("You passed the challenge!")
else:
  print("You haven't passed yet. Your model should identify at least 63% of the images. Keep trying. You will get it!")