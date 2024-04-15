import cv2
import numpy as np
# from safetensors import SafeTensors
import timm 
import torch
import torchvision.transforms as transforms
# Load model directly
from transformers import AutoConfig, AutoModelForObjectDetection

config = AutoConfig.from_pretrained("driesverachtert/basic_shapes_object_detection")
model = AutoModelForObjectDetection.from_pretrained("driesverachtert/basic_shapes_object_detection")

def extract_image_data(move):
    path = move['path']

    # Assuming a white background
    img = np.zeros((400, 400, 3), dtype=np.uint8)  # Example: Create a 400x400 image
    img.fill(255)  # Fill with white

    # Draw the shape based on coordinates (you might need to adjust this)
    for i in range(len(path) - 1):
        start_point = path[i]
        end_point = path[i + 1]
        cv2.line(img, start_point, end_point, color=(0, 0, 0), thickness=2)  # Draw black line

    return img


def detect_shapes(move):
    img = extract_image_data(move) 

    # Preprocessing
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)), 
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    input_tensor = transform(image)
    input_tensor = input_tensor.unsqueeze(0) 

    # Inference
    with torch.no_grad():
        outputs = model(input_tensor)

    # Extract detected shapes
    detected_shapes = []  
    print(f"this is outputs: {outputs}")
    # AI IMPLEMENTATION
    # labels = outputs.argmax(1).squeeze().tolist()
    # Mine
    labels = torch.argmax(outputs.logits, dim=2).squeeze().tolist()
    for label in labels:
        if label == 0:
            detected_shapes.append('circle')
        elif label == 1:
            detected_shapes.append('rectangle')
        elif label == 2:
            detected_shapes.append('triangle')

    print(f"This is all the detected shapes: {detected_shapes}")
    return detected_shapes 
