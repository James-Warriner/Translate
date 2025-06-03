import easyocr
import cv2
import numpy as np

from helpers import returnError

def get_image(request):
  if "image" not in request.files:
    return returnError("No image")
  
  img_file = request.files["image"]
  img_bytes = img_file.read()

  return img_bytes
  


_readers: dict[str, easyocr.Reader] = {}

def get_reader(src_lang: str) -> easyocr.Reader:
    """
    Return a singleton EasyOCR Reader for the given source language code.
    """
    if src_lang not in _readers:

        _readers[src_lang] = easyocr.Reader([src_lang])
    return _readers[src_lang]

def preProcessImage(image_bytes: bytes, src_code: str) -> str:


    nparr = np.frombuffer(image_bytes, dtype=np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image bytes")


    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    reader = get_reader(src_code)

    result = reader.readtext(gray)

    extracted_words: list[str] = []
    for item in result:
        if len(item) == 3:
            _, text, conf = item
        elif len(item) == 2:
            _, text = item
            conf = None
        else:
            continue

        if conf is not None and conf < 0.3:
            continue

        extracted_words.append(text)

    return " ".join(extracted_words).strip()
