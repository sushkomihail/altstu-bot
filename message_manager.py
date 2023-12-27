import os
import text_recognizer


def is_number_correct(number: str, minimum: int, maximum: int) -> bool:
    return number.isdigit() and minimum <= int(number) <= maximum


def get_photos(file_path: str) -> list:
    try:
        return os.listdir(path=file_path)
    except FileNotFoundError:
        return []


def get_photos_by_text(file_path: str, text: str) -> list:
    photos = get_photos(file_path)
    input_words = text.split()
    result = []

    if len(photos) == 0 or len(input_words) == 0:
        return result

    for photo in photos:
        directory = f'{file_path}/{photo}'
        recognized_words = text_recognizer.get_recognized_text_words(directory)
        compares_count = 0

        for word in input_words:
            if word in recognized_words:
                compares_count += 1

        if compares_count / len(input_words) >= 0.75:
            result.append(photo)
    return result
