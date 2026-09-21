import sys
import os

import pytesseract
from PIL import Image, ImageDraw

# --- Windows only: uncomment and set this if pytesseract can't find
# Tesseract automatically. Leave commented out on Mac/Linux.
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

OUTPUT_DIR = "output"


def recognize_text(image_path: str):
    if not os.path.exists(image_path):
        print(f"Error: file not found -> {image_path}")
        sys.exit(1)

    print(f"Reading: {image_path}")
    image = Image.open(image_path)

    # --- Step 1: the recognized text itself ---
    text = pytesseract.image_to_string(image)

    print("\n" + "=" * 50)
    print("TEXT FOUND IN THE IMAGE")
    print("=" * 50)
    print(text.strip() if text.strip() else "(no text detected)")

    # --- Step 2: word-level confidence + bounding boxes ---
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    annotated = image.convert("RGB").copy()
    draw = ImageDraw.Draw(annotated)

    print("\n" + "=" * 50)
    print("CONFIDENCE PER WORD")
    print("=" * 50)

    found_any = False
    for i in range(len(data["text"])):
        word = data["text"][i].strip()
        conf = int(data["conf"][i])
        if word and conf > 0:
            found_any = True
            print(f"{word:<25}{conf:>3}%")
            x, y, w, h = (data["left"][i], data["top"][i], data["width"][i], data["height"][i])
            draw.rectangle([x, y, x + w, y + h], outline=(255, 0, 0), width=2)

    if not found_any:
        print("(no words detected)")

    # --- Step 3: save the annotated version in the output/ folder ---
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    file_name = os.path.basename(image_path)
    name_only, _ = os.path.splitext(file_name)
    annotated_path = os.path.join(OUTPUT_DIR, f"{name_only}_annotated.png")
    annotated.save(annotated_path)
    print(f"\nAnnotated image saved to: {annotated_path}")

    return text


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 recognize_image.py path/to/your_picture.jpg")
        sys.exit(1)

    recognize_text(sys.argv[1])
