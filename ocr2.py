import cv2
import os
import os.path
import json
import pytesseract
import re
from PIL import Image, ImageEnhance, ImageFilter
import PIL
# from matplotlib import pyplot as plt

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'


# img_path = 'D:\\finalimage.jpg'

def preprocess(img):

    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    cordinates = [cordinate[0] for contour in contours[1:] for cordinate in contour]
    values = [cordinate[0][0]+cordinate[0][1] for contour in contours[1:] for cordinate in contour]
    x,y = cordinates[values.index(min(values))]
    w,h = cordinates[values.index(max(values))]
    padding = 20

    cropped_image = imgray[x:h, y:w]

    cv2.rectangle(img,(x-padding,y-padding),(w+padding,h+padding),(0,255,0),5)

    pil_img = cv2.cvtColor(imgray,cv2.COLOR_BGR2RGB)
    img = Image.fromarray(pil_img, 'RGB')
    img = ImageEnhance.Contrast(img).enhance(2)
    # return img
    return thresh

def get_text(img):
    texttest = pytesseract.image_to_string(img)

    texttest = texttest.lower()
    texttest = re.sub("government of india","",texttest)
    # print(texttest)
    lines = [texttest.split("\n")]

    dob_pattern = re.compile('\d{2}/\d{2}/\d{4}')
    # mob_pattern = re.compile('mobile no.*?\n')
    mob_pattern = re.compile('\d{10}')
    # gender_pattern = re.compile('..male\n')
    # gender_pattern = re.compile('\w{0,2}male\n')
    gender_pattern = re.compile('(fe){0,1}male')
    adhar_pattern = re.compile('\d{4} \d{4} \d{4}')
    # father_pattern = re.compile('father(?s).*?\n')

    dob = adhaar_no = gender = mob_no = None
    dob_line = -1
    for i in range(len(lines[0])):
        line = lines[0][i]
        # print(line)
        if dob == None:
            dob = re.search(dob_pattern,line)
            dob_line = i
        if adhaar_no == None:
            adhaar_no = re.search(adhar_pattern,line)
        if gender == None:
            gender = re.search(gender_pattern,line)
        if mob_no == None:
            mob_no = re.search(mob_pattern,line)
    name = lines[0][dob_line-1]
    name = name.strip()

    # print(f"{name}-{dob[0]}-{gender[0]}-{mob_no}-{adhaar_no}")

    if mob_no!=None:
        mob_no = mob_no[0]

    details = {"name" : name,
            "dob" : dob[0],
            "gender": gender[0],
            "ph_no." : mob_no,
            "adhaar_no" : adhaar_no[0]
            }
    print(details)
    return details

def main_ocr(cropped,output_folder):

    # input_folder = "input\\"
    # output_folder = "output\\"
    # for files in os.listdir(f"{os.getcwd()}\\{input_folder}"):
        # img_path = f"{os.getcwd()}\\input\\{files}"

    # print(img_path)
    # img = cv2.imread(img_path)
    img = cropped
    img = preprocess(img)
    details = get_text(img)
    # img_path = "input\\myad2.jpg"


    with open(f"{output_folder}details.json","a") as file:
        json_str = json.dumps(details)+"\n"
        file.write(json_str)
        file.close()

# if __name__=="__main__":
#     main()
