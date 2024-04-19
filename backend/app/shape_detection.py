import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

# Load the TensorFlow/Keras model. 
model = keras.models.load_model('model/shapedetector_model_t2.h5')

class_names = ['circle', 'rectangle', 'square', 'triangle']

def extract_image_data(move, margin=20):
    path = move['path']

    # Assuming a white background
    path = move['path']

    # Calculate the bounding box of the path
    min_x = min(point[0] for point in path)
    max_x = max(point[0] for point in path)
    min_y = min(point[1] for point in path)
    max_y = max(point[1] for point in path)

    # Calculate image dimensions based on the bounding box plus a margin
    img_width = max_x - min_x + margin * 2
    img_height = max_y - min_y + margin * 2

    # Create an image with a white background
    img = np.zeros((img_height, img_width, 3), dtype=np.uint8)
    img.fill(255)

    # Calculate the shift needed to center the drawing in the new image
    shift_x = margin - min_x
    shift_y = margin - min_y

    # Draw the shape based on shifted coordinates
    for i in range(len(path) - 1):
        start_point = (path[i][0] + shift_x, path[i][1] + shift_y)
        end_point = (path[i + 1][0] + shift_x, path[i + 1][1] + shift_y)
        cv2.line(img, start_point, end_point, (0, 0, 0), 2)

    cv2.imwrite('dynamic_output_image.png', img)
    return img

def detect_shapes(move):
    img = extract_image_data(move)

    # Convert to grayscale and resize for the model
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (28, 28))

    # Normalize the image to match the input requirements of the model
    img_array = np.array(img) / 255.0
    img_array = img_array.reshape(1, 28, 28, 1)  # Reshape for the model (adding batch dimension)

    # Perform prediction
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    # Decode the predictions
    predicted_label = class_names[np.argmax(score)]
    confidence = np.max(score)

    print(f"Detected shape: {predicted_label} with confidence: {confidence:.2f}")
    return [predicted_label, confidence]