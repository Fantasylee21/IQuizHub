import base64
import os
import uuid

from paddleocr import PaddleOCR, draw_ocr
from PIL import Image


def ocr(base64_img: str):
    img_data = base64.b64decode(base64_img)

    image_folder = 'temp_images'
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    file_name = f"{uuid.uuid4().hex}"
    file_path = os.path.join(image_folder, file_name)

    with open(file_path, 'wb') as f:
        f.write(img_data)
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")
    img_path = file_path
    result = ocr.ocr(img_path, cls=True)

    result = result[0]
    image = Image.open(img_path).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
    im_show = Image.fromarray(im_show)
    return im_show, txts
