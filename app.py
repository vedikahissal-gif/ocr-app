from flask import Flask, render_template, request
import pytesseract
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""

    if request.method == "POST":
        file = request.files["image"]

        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            try:
                text = pytesseract.image_to_string(Image.open(file_path))
            except:
                text = "OCR failed. Tesseract may not be installed."

    return render_template("index.html", text=text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)