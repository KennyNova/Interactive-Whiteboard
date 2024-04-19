import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.losses import CategoricalCrossentropy

# Load the TensorFlow/Keras model. 
model = keras.models.load_model('model/shapedetector_model_4b.h5', compile=False)

model.compile(optimizer='adam',
              loss=tf.keras.losses.CategoricalCrossentropy(reduction=tf.keras.losses.Reduction.SUM_OVER_BATCH_SIZE),
              metrics=['sum_over_batch_size'])

tf.saved_model.save('model/shapedetector_model_t2_FIXED.h5')

# tf.compat.v1.keras.models.save_model(model, 'shapedetector_model_t2_FIXED.h5')
