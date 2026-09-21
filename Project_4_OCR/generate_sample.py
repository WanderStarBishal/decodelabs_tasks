import os
from PIL import Image, ImageDraw, ImageFont

# Common bold font locations across platforms. The first one that
# exists on this machine will be used; if none are found, PIL's
# built-in default font is used instead so the script never crashes.
CANDIDATE_FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
    "C:\\Windows\\Fonts\\arialbd.ttf",                        # Windows (Arial Bold)
    "C:\\Windows\\Fonts\\Arial.ttf",                          # Windows fallback
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",     # Mac
    "/Library/Fonts/Arial Bold.ttf",                          # Mac fallback
]


def _find_font():
    for path in CANDIDATE_FONT_PATHS:
        if os.path.exists(path):
            return path
    return None


FONT_PATH = _find_font()
LINES = [
    "Basic Text Recognition Demo",
    "Library used: Tesseract OCR (pytesseract)",
    "Sample Input Image 2026",
    "1234567890 - OCR Test",
]


def generate_sample_image(path="sample_input.png"):
    width, height = 640, 260
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    if FONT_PATH:
        font_title = ImageFont.truetype(FONT_PATH, 28)
        font_body = ImageFont.truetype(FONT_PATH, 22)
    else:
        # No known font found on this system -- fall back to PIL's
        # built-in bitmap font so the script still runs.
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()

    y = 30
    for i, line in enumerate(LINES):
        font = font_title if i == 0 else font_body
        draw.text((30, y), line, font=font, fill=(0, 0, 0))
        y += 50

    img.save(path)
    print(f"Sample image saved to: {path}")
    return path


if __name__ == "__main__":
    generate_sample_image()