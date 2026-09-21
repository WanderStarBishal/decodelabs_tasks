import argparse
import os

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from PIL import Image, ImageDraw

from generate_sample import generate_sample_image

OUTPUT_DIR = "output"


def run_recognition(image_path: str):
    print(f"\nLoading image: {image_path}")
    image = Image.open(image_path)

    # --- Step 1: plain extracted text (the simplest model output) ---
    extracted_text = pytesseract.image_to_string(image)

    print("\n" + "=" * 50)
    print("RECOGNIZED TEXT")
    print("=" * 50)
    print(extracted_text.strip())

    # --- Step 2: structured output (word-level boxes + confidences) ---
    # image_to_data gives us the model's internal predictions per word:
    # position, size, and a confidence score (0-100, -1 = no text found).
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    print("\n" + "=" * 50)
    print("WORD-LEVEL CONFIDENCE (model output detail)")
    print("=" * 50)
    print(f"{'Word':<25}{'Confidence':>10}")
    print("-" * 35)

    annotated = image.convert("RGB").copy()
    draw = ImageDraw.Draw(annotated)

    n_boxes = len(data["text"])
    recognized_words = 0
    confidences = []

    for i in range(n_boxes):
        word = data["text"][i].strip()
        conf = int(data["conf"][i])
        if word and conf > 0:
            recognized_words += 1
            confidences.append(conf)
            print(f"{word:<25}{conf:>9}%")

            x, y, w, h = (
                data["left"][i],
                data["top"][i],
                data["width"][i],
                data["height"][i],
            )
            draw.rectangle([x, y, x + w, y + h], outline=(255, 0, 0), width=2)

    avg_conf = sum(confidences) / len(confidences) if confidences else 0

    print("-" * 35)
    print(f"Words recognized : {recognized_words}")
    print(f"Average confidence: {avg_conf:.1f}%")

    # --- Step 3: save outputs so results are clearly visible ---
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    annotated_path = os.path.join(OUTPUT_DIR, "annotated_output.png")
    annotated.save(annotated_path)

    text_path = os.path.join(OUTPUT_DIR, "extracted_text.txt")
    with open(text_path, "w") as f:
        f.write(extracted_text.strip() + "\n")

    print("\nSaved annotated image to:", annotated_path)
    print("Saved extracted text to :", text_path)

    return extracted_text, avg_conf


def main():
    parser = argparse.ArgumentParser(description="Basic text recognition using Tesseract OCR")
    parser.add_argument(
        "--image",
        type=str,
        default=None,
        help="Path to an input image. If omitted, a sample image is generated.",
    )
    args = parser.parse_args()

    image_path = args.image
    if image_path is None:
        image_path = generate_sample_image("sample_input.png")

    run_recognition(image_path)


if __name__ == "__main__":
    main()
