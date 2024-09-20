import torch
from torchvision import transforms
from PIL import Image
import cv2
from os import listdir
import numpy as np
import matplotlib as plt


def load_image(image_path):
    image = cv2.imread(image_path)
    return image

def load_east_model():  # pretrained EAST model
    model = torch.hub.load('pytorch/vision:v0.10.0', 'fasterrcnn_resnet50_fpn', pretrained=True)
    model.eval()
    return model

def detect_text_east(image_path, model): # detect text using EAST
    image = Image.open(image_path)
    transform = transforms.Compose([transforms.ToTensor(),])
    image_tensor = transform(image).unsqueeze(0)  # add batch dimension

    with torch.no_grad(): # perform inference
        predictions = model(image_tensor)

    return predictions

def display_image(image, title="Image"):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis("off")
    plt.show()

def get_bounding_boxes_from_predictions(predictions): # predictions 2 bounding boxes
    boxes = predictions[0]['boxes'].cpu().numpy()  # extract bounding boxes from predictions
    return boxes

def draw_boxes_east(image_path, boxes): # draw bounding boxes on image
    image = cv2.imread(image_path)
    for box in boxes:
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    display_image(image, title="Image with Deep Learning Detected Text")
    return image


def main(image_path):
    model = load_east_model() # Load EAST
    predictions = detect_text_east(image_path, model) # Detect text
    boxes = get_bounding_boxes_from_predictions(predictions)

    draw_boxes_east(image_path, boxes) # Draw boxes
    image = load_image(image_path) # inpainting

    mask = np.zeros_like(image[:, :, 0]) # Create a mask
    for box in boxes:
        x1, y1, x2, y2 = map(int, box)
        mask[y1:y2, x1:x2] = 255

    inpainted_image = cv2.inpaint(image, mask, inpaintRadius=5, flags=cv2.INPAINT_TELEA)
    display_image(inpainted_image, title="Image After Text Removal with EAST Model")
    return inpainted_image


for images in listdir('C:Users/user/pythonProject'):
    processed_image = main(images)
