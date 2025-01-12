import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow import keras
from keras import layers
from keras.models import Sequential

import pickle


# define dataset file path
data_train_path = 'backend/model/data/train'
data_test_path = 'backend/model/data/test'

# define img size
img_width = 180
img_height = 180

# retrieve training images from train folder
data_train = tf.keras.utils.image_dataset_from_directory(
    data_train_path,
    shuffle=True,
    image_size=(img_width, img_height),
    batch_size=32,
    validation_split=False
)

# retrieve category names
data_categories = data_train.class_names

# Reserve 20% for validation
val_size = int(0.2 * len(data_train))  
train_size = len(data_train) - val_size

data_val = data_train.take(val_size)
data_train = data_train.skip(val_size)


# take image from train dataset
data_test = tf.keras.utils.image_dataset_from_directory(
    data_test_path,
    shuffle=True,
    image_size=(img_width, img_height),
    batch_size=32,
    validation_split=False
)

# define plot size
plt.figure(figsize=(10,10))

# # plot a single image from each category
# for image, labels in data_train.take(1):
#     for i in range(9):
#         plt.subplot(3,3,i+1)
#         plt.imshow(image[i].numpy().astype('uint8'))
#         plt.title(data_categories[labels[i]])
#         plt.axis('off')
#         plt.show()

# improve generalization and reduce overfitting
data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])

# create sequential model
model = Sequential([
    data_augmentation,
    layers.Rescaling(1/255),
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.BatchNormalization(),  # Add BatchNormalization
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dropout(0.2),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(data_categories), activation='softmax')
])



# compile model
model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False), metrics=['accuracy'])

# define epoch
epoch_size = 25

# train the model
history = model.fit(data_train, validation_data=data_val, epochs=epoch_size, verbose=1)

# Plot training and validation metrics
plt.figure(figsize=(12, 4))

# Accuracy plot
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend()
plt.title('Accuracy')

# Loss plot
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend()
plt.title('Loss')

# plt.show()

model_architecture = model.to_json()
model_weights = model.get_weights()

with open('model.pkl', 'wb') as f:
    pickle.dump({'architecture': model_architecture, 'weights': model_weights}, f)

# Make predictions on the test dataset
predictions = model.predict(data_test)

# Convert probabilities to percentages
percentages = predictions * 100

# Print percentages for the first batch of images
for i, preds in enumerate(percentages[:10]):  # Show results for the first 10 images
    print(f"Image {i+1}:")
    for category, percentage in zip(data_categories, preds):
        print(f"  {category}: {percentage:.2f}%")
    print()