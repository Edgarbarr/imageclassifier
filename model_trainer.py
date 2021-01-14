#!/usr/bin/env python3
import tensorflow as tf

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.layers import Conv2D, MaxPool2D, Flatten, Dense

train = ImageDataGenerator(rescale=1 / 255)
validation = ImageDataGenerator(rescale=1 / 255)

train_dataset = train.flow_from_directory("dataset/train/", target_size=(200, 200), batch_size=10, class_mode="binary")

validation_dataset = train.flow_from_directory("dataset/validation/", target_size=(200, 200), batch_size=3,
                                               class_mode="binary")
print(train_dataset.class_indices)
cat0 = None
cat1 = None
for key in train_dataset.class_indices:
    if train_dataset.class_indices[key] == 0:
        cat0 = key
    else:
        cat1 = key

model = tf.keras.models.Sequential([Conv2D(16, (3, 3), activation='relu', input_shape=(200, 200, 3)),
                                    MaxPool2D(2, 2),
                                    Conv2D(32, (3, 3), activation='relu', input_shape=(200, 200, 3)),
                                    MaxPool2D(2, 2),
                                    Conv2D(64, (3, 3), activation='relu', input_shape=(200, 200, 3)),
                                    MaxPool2D(2, 2),
                                    Flatten(),
                                    Dense(512, activation="relu"),
                                    Dense(1, activation="sigmoid")])

model.compile(loss="binary_crossentropy", optimizer=RMSprop(lr=0.001), metrics=["accuracy"])

model_fit = model.fit(train_dataset, steps_per_epoch=3, epochs=30, validation_data=validation_dataset)
