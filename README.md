# Adhaar Card Details Extraction
This Python 3-based project uses YOLOv8 (You Only Look Once version 8) for the detection of Aadhaar cards in images, followed by the extraction of key details such as the Aadhaar number, name, and address. <br>
Please check <a href="https://github.com/ultralytics/ultralytics/tree/main "> YOLOV8 doumentation</a> for details and installing YOLOv8. <br>
Python version - <a href = "https://docs.python.org/3.9/"> Python >= 3.9</a>

Dependencies: <br>
- Python 3.x
- YOLOv8
- OpenCV
- pytesseract (for OCR)
- NumPy

```
pip install requirements.txt
```

<b>Features</b>: <br>
- Aadhaar Card Detection: Uses YOLOv8 for efficient and accurate detection of Aadhaar cards in a variety of image formats.
- Information Extraction: Extracts key details like Aadhaar number, name, and address from the detected Aadhaar card.
- Preprocessing: Supports image preprocessing for better accuracy, including resizing, normalization, and noise reduction.

Usage:
- Clone the repository and install the required dependencies.
- Run the program, providing an image or a folder of images containing Aadhaar cards.
- The program will detect the card and output the extracted details in a structured format (JSON or CSV).

The model is pre trained on adhaar card images that are freely available on google.
PS. The model does not work on any other documents like PAN Card and will give output as INVALID ID in those cases.
