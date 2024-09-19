import cv2
import numpy as np
import pytesseract
from matplotlib import pyplot as plt
from os import listdir

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def load_image(image_path):
    image = cv2.imread(image_path)
    return image


def display_image(image, title="Image"):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis("off")
    plt.show()


def detect_text(image):  # detect text via Tesseract OCR
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    boxes = pytesseract.image_to_boxes(gray)

    return boxes


def draw_text_boxes(image, boxes):  # draw the box around the number
    for box in boxes.splitlines():
        b = box.split(' ')
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(image, (x, image.shape[0] - y), (w, image.shape[0] - h), (0, 255, 0), 2)
    return image


def remove_text_inpaint(image, boxes): # mask text areas and use inpainting to remove text
    mask = np.zeros_like(image[:, :, 0])

    for box in boxes.splitlines():
        b = box.split(' ')
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        mask[image.shape[0] - y:image.shape[0] - h, x:w] = 255
    inpainted_image = cv2.inpaint(image, mask, inpaintRadius=5, flags=cv2.INPAINT_TELEA)

    return inpainted_image


def main(image_path): # apply the functions here
    image = load_image(image_path)
    display_image(image, title="Original Image")

    boxes = detect_text(image)

    boxed_image = draw_text_boxes(image.copy(), boxes)
    display_image(boxed_image, title="Image with Text Boxes")

    inpainted_image = remove_text_inpaint(image, boxes)

    display_image(inpainted_image, title="Image After Text Removal")

    return inpainted_image


for image_path in listdir('path_to_your_image'):
    image_path = 'path_to_your_image.jpg' # test the pipeline on an example image
    processed_image = main(image_path)

