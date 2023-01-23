# -*- coding: utf-8 -*-
"""UrbanSoundsCV.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dmiYGRZbBcwdxfuqC-TD198V4IZJL2Oe
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
from sklearn.preprocessing import LabelEncoder, minmax_scale
from sklearn.model_selection import train_test_split 
import tensorflow as tf



DATADIR="/content/drive/MyDrive/spectrograms"
CATEGORIES = [0,1,2,3,4,5,6,7,8,9]
dataset=[]
IMG_SIZE=50
for category in CATEGORIES:  
    path = os.path.join(DATADIR,str(category))  
    class_num = category
    for img in os.listdir(path): 
        img_array = cv2.imread(os.path.join(path,img) ,cv2.IMREAD_GRAYSCALE)  
        new_array = cv2.resize(img_array,(IMG_SIZE,IMG_SIZE))
        dataset.append([new_array,class_num])

X=[]
y=[]



for features,label in dataset:
  X.append(features)
  y.append(label)
X = np.array(X).reshape(-1,IMG_SIZE,IMG_SIZE,1)

X_train, X_temporary, y_train, y_temporary = train_test_split(X, y, train_size = 0.8)

X_val, X_test, y_val, y_test = train_test_split(X_temporary, y_temporary, train_size = 0.5)

print("Data ",len(X))
print("train ",len(X_train))
print("val ", len(X_val))
print("test ", len(X_test))

X_test=X_test/255
X_train=X_train/255
X_val = X_val/255

model = tf.keras.Sequential()

model.add(tf.keras.layers.Conv2D(32,
                                 kernel_size=(3,3),
                                 strides=(1,1),
                                 padding='same',
                                 activation='relu',
                                 input_shape=(50,50,1)))
model.add(tf.keras.layers.MaxPooling2D((2,2)))

model.add(tf.keras.layers.Conv2D(64,
                                 kernel_size=(3,3),
                                 strides=(1,1),
                                 padding='same',
                                 activation='relu',
                                 input_shape=(50,50,1)))
model.add(tf.keras.layers.MaxPooling2D((2,2)))
model.add(tf.keras.layers.Conv2D(64,
                                 kernel_size=(3,3),
                                 strides=(1,1),
                                 padding='same',
                                 activation='relu',
                                 input_shape=(50,50,1)))

model.add(tf.keras.layers.Flatten())

# Add the dense layer and dropout layer
model.add(tf.keras.layers.Dense(64, activation = 'relu'))
model.add(tf.keras.layers.Dropout(0.5))

# Add the dense layer and dropout layer
model.add(tf.keras.layers.Dense(64, activation = 'relu'))
model.add(tf.keras.layers.Dropout(0.5))

model.add(tf.keras.layers.Dense(10, activation = 'softmax'))



model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics= ["accuracy"])

X_val=np.array(X_val)
X_train=np.array(X_train)
X_test=np.array(X_test)
y_val=np.array(y_val)
y_train=np.array(y_train)
y_test=np.array(y_test)

results= model.fit(X_train, y_train,
                   batch_size = 128,
                   epochs=50,
                   validation_data=(X_val, y_val))

# Plot the the training loss
plt.plot(results.history["loss"],label="loss")

# Plot the the validation loss
plt.plot(results.history["val_loss"],label="val_loss")


# Name the x and y axises
plt.xlabel("Epoch")
plt.ylabel("Loss")

# Put legend table
plt.legend()

# Show the plot
plt.show()

# Plot the the training accuracy
plt.plot(results.history["accuracy"],label="accuracy")

# Plot the the validation accuracy
plt.plot(results.history["val_accuracy"], label= 'val_accuracy')

# Name the x and y axises
plt.xlabel("Epoch")
plt.ylabel("Accuracy")

# Put legend table
plt.legend()

# Show the plot
plt.show()