from ultralytics import YOLO
import os
import pytesseract
import cv2
from matplotlib import pyplot as plt
import math
from typing import Tuple, Union
import numpy as np
from deskew import determine_skew
import ocr2

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'


def rotate(
        image: np.ndarray, angle: float, background: Union[int, Tuple[int, int, int]]
) -> np.ndarray:
    old_width, old_height = image.shape[:2]
    angle_radian = math.radians(angle)
    width = abs(np.sin(angle_radian) * old_height) + abs(np.cos(angle_radian) * old_width)
    height = abs(np.sin(angle_radian) * old_width) + abs(np.cos(angle_radian) * old_height)

    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    rot_mat[1, 2] += (width - old_width) / 2
    rot_mat[0, 2] += (height - old_height) / 2
    return cv2.warpAffine(image, rot_mat, (int(round(height)), int(round(width))), borderValue=background)


def check_validity(input_dir,model_path):
    model = YOLO(model_path)
    flag = 0
    # for images in os.listdir(input_dir):
    #     img_path = f"{input_dir}{images}"
    try:
        results = model([input_dir])
        # print(results)
        classes_predict = [model.names[int(c)] for r in results for c in r.boxes.cls]
        if 'adhaar' in classes_predict:
            flag = 1
        else:
            flag = 0
    except:
        flag = -1
    return [flag,results]

def main():
    model_path = "weights\\best.pt"
    input_dir = "test_images\\"
    output_dir = "output\\"
    out_dict = {-1 : "Error In Input",
               0 : "Not Adhaar Image",
               1 : "Adhaar Card Detected"}
    
    for images in os.listdir(input_dir):
        img_path = f"{os.getcwd()}\\{input_dir}{images}"
        image = cv2.imread(img_path)
        # print(img_path)
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    angle = determine_skew(grayscale)
    rotated = rotate(image, angle, (0, 0, 0))
    cv2.imwrite(f"{output_dir}rotated.jpg",rotated)

    validity = check_validity(f"{output_dir}rotated.jpg",model_path)

    print(out_dict[validity[0]])
    
    if validity[0]==1:
        x,y,w,h = validity[1][0].boxes.xyxy[0]
        a,b,c = image.shape
        x_padding,y_padding = int(0.05*a),int(0.05*b)
        # cropped = rotated[int(y):int(h),int(x):int(w)]
        cropped = rotated[int(y)-x_padding:int(h)+x_padding,int(x)-y_padding:int(w)+y_padding]
        # plt.imshow(cropped)
        # img = cv2.imread(f"{input_dir}26b187cff97638ee0753d56c52c09bde.png")
        # cropped = img[int(y):int(h),int(x):int(w)]
        cv2.imwrite(f"{output_dir}cropped.png",cropped)
        # rotation_correction.rotation_main(input_dir,output_dir)
        ocr2.main_ocr(cropped,output_dir)


if __name__=="__main__":
    main()
