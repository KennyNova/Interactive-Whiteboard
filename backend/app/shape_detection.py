import cv2
import numpy as np
import timm 
import torch
import torchvision.transforms as transforms, Compose, ToPILImage, Resize, ToTensor, Normalize
from transformers import AutoConfig, AutoModelForObjectDetection, AutoTokenizer



config = AutoConfig.from_pretrained("driesverachtert/basic_shapes_object_detection")
model = AutoModelForObjectDetection.from_pretrained("driesverachtert/basic_shapes_object_detection")

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

    # Process the model's output
    results = outputs['logits'][0]  # Taking the first (and only) batch
    keep = results[:, -1] < 0.9  # Keep predictions where the 'no object' class score is low

    # Decode bounding boxes and labels
    scores = results[keep, -1]
    labels = results[keep, :-1].argmax(1)
    boxes = outputs['pred_boxes'][0][keep]

    print(scores, labels)

    detected_shapes = []
    for score, label, box in zip(scores, labels, boxes):
        if score > 0.85:  # Confidence threshold
            shape_label = 'square' if label == 0 else 'circle' if label == 1 else 'triangle'
            detected_shapes.append((shape_label, box.tolist(), score.item()))

    print(f"This is all the detected shapes: {detected_shapes}")
    return detected_shapes
