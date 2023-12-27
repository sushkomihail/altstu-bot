import pytesseract
from PIL import Image
from settings import *

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

SYMBOLS = '.!@"$#№;:*?&^(){}[]-=+<>,©|'


def get_recognized_text_words(file_path: str) -> list:
    img = Image.open(file_path)
    text = pytesseract.image_to_string(img, lang='rus', config=TESSERACT_CONFIG)
    return get_formatted_text_words(text)


def get_formatted_text_words(text: str) -> list:
    text = text.lower()

    for symbol in SYMBOLS:
        text = text.replace(symbol, '')

    formatted_text_words = ' '.join(list(map(lambda x: x.strip(), text.split('\n')))).split()
    return formatted_text_words
