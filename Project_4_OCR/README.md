# Text Recognition Project (OCR)

A small Python project that reads text out of images using **Tesseract OCR**,
a pre-trained open-source text recognition engine, accessed through the
`pytesseract` library.

There are **two separate programs** in this folder — they don't call each
other, and neither replaces the other:

| File | What it's for |
|---|---|
| `recognize_image.py` | **Use this one.** Give it any picture of your own, it prints the text found in it. |
| `main.py` | A self-contained demo: generates its own sample image, then runs OCR on it. Useful for showing the assignment end-to-end without needing an external photo. |

---

## Folder structure

```
text_recognition_project/
├── main.py                 → the demo (uses generate_sample.py + saves to output/)
├── generate_sample.py      → helper, only called by main.py, never run directly
├── recognize_image.py      → run this on YOUR OWN pictures
├── requirements.txt        → Python libraries to install
├── README.md                → this file
├── sample_input.png        → example image created by generate_sample.py
└── output/                 → results from running main.py land here
    ├── annotated_output.png
    └── extracted_text.txt
```

When you run `recognize_image.py` on a picture, its annotated result is also
saved into `output/`, named `yourfile_annotated.png` (based on your original
file's name).

---

## Setup (do this once)

### 1. Install the Tesseract OCR engine
This is the actual recognition model — a system program, not a Python package.

- **Windows:** download the installer from
  [UB-Mannheim's Tesseract build](https://github.com/UB-Mannheim/tesseract/wiki)
  and run it. Note the install folder (default: `C:\Program Files\Tesseract-OCR`).
- **Mac (Homebrew):** `brew install tesseract`
- **Ubuntu / Debian / WSL:** `sudo apt-get update && sudo apt-get install -y tesseract-ocr`

Check it worked by running `tesseract --version` in a terminal.

### 2. Install the Python libraries
From inside this folder:
```
pip install -r requirements.txt
```
This installs `pytesseract` (the Python wrapper) and `Pillow` (image handling).

### 3. Windows only — point pytesseract at Tesseract
On Windows, Python sometimes can't find `tesseract.exe` automatically. Open
`recognize_image.py` (and `main.py` if you use it), find this line near the
top, and remove the `#` in front of it:
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```
Make sure the path matches where Tesseract actually installed on your machine
(run `where tesseract` in a terminal to check). Mac/Linux users can skip this.

---

## Usage

### Read text from your own picture
```
python3 recognize_image.py path/to/your_picture.jpg
```
- If the picture is in this same folder, just use its file name.
- If it's elsewhere, give the full path instead.

**Output:**
- Prints the recognized text to the terminal
- Prints a confidence score (0–100%) for every word found
- Saves `output/your_picture_annotated.png`, with red boxes drawn around
  every recognized word

### Run the assignment demo
```
python3 main.py
```
Generates its own sample image, runs OCR on it, and saves results into
`output/annotated_output.png` and `output/extracted_text.txt`.

You can also point the demo at your own image instead of the generated one:
```
python3 main.py --image path/to/your_picture.jpg
```

---

## Understanding the output

Tesseract doesn't just return one block of text — for every word it finds,
it also returns:
- **Position** (a bounding box: x, y, width, height)
- **Confidence** (0–100, how sure the model is that it read the word correctly)

Both scripts print this per-word confidence and draw the bounding boxes onto
a saved image, so you can see *where* the model looked and *how sure* it was
— not just its final guess.

---

## Troubleshooting

**`TesseractNotFoundError: tesseract is not installed or it's not in your PATH`**
Tesseract the engine isn't installed, or Python can't find it. Do step 1 and
step 3 above — installing `pytesseract` alone is not enough, it just talks to
the real engine.

**`OSError` / font error from `generate_sample.py`**
Only affects `main.py`'s sample-image generator. It looks for a bold font in
common system locations; if your system has none of them, it falls back to a
basic built-in font automatically — this doesn't affect `recognize_image.py`
at all, since that script doesn't generate any images.

**Recognized text looks wrong or confidence is low**
Usually means the image is blurry, low-resolution, at an angle, or has a
busy background. OCR engines like Tesseract work best on clear, front-on,
well-lit text (like a scanned document or a clean screenshot).

---

## How this satisfies the assignment spec

| Requirement | How it's met |
|---|---|
| Use a pre-trained model or simple library | Tesseract OCR (pre-trained), via `pytesseract` |
| Perform recognition on sample input | `main.py` generates and reads a sample image; `recognize_image.py` reads any image you give it |
| Display the output clearly | Console text + per-word confidence scores + annotated image with bounding boxes |
| Using AI libraries | `pytesseract`, `Pillow` |
| Understanding model outputs | Per-word confidence scores are shown, not just the final text |
