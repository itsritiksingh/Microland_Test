import io
from typing import List
import uuid
from pdf2image import convert_from_bytes
import pytesseract
import os
from PIL import Image

from src.utils.langchain import generate_embedding


def perform_ocr_on_images(num_pages: List[str]):

    combined_text = ""

    for i in range(len(num_pages)):
        image_path = num_pages[i]
        image = Image.open(image_path)

        text = pytesseract.image_to_string(image)
        combined_text += text + "\n"
        dummy_file_name = f"{uuid.uuid4()}.txt"
        extracted_text = os.path.join("src/static/texts", dummy_file_name)

        with open(extracted_text, "w") as f:
            f.write(combined_text)

        print(f"Extraction complete. Text saved to {extracted_text}")
        return extracted_text, dummy_file_name


def convert_pdf_to_images(pdf: io.BytesIO):
    pages = convert_from_bytes(pdf)
    images_paths = []

    for i, page in enumerate(pages):
        path = f"src/static/images/page_{i}.jpg"
        page.save(path, "JPEG")
        images_paths.append(path)

    extracted_text, dummy_file_name = perform_ocr_on_images(images_paths)
    generate_embedding(extracted_text)
    return dummy_file_name
