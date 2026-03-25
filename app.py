from flask import Flask, render_template, request, send_file
import pandas as pd
import re
import requests
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def ocr_api(image_path):
    url = "https://api.ocr.space/parse/image"

    with open(image_path, 'rb') as f:
        response = requests.post(url, files={"file": f})

    result = response.json()
    return result["ParsedResults"][0]["ParsedText"]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        text = ocr_api(path)

        # extract emails & phones
        emails = re.findall(r'\S+@\S+', text)
        phones = re.findall(r'\d{10}', text)

        data = []
        for i in range(min(len(emails), len(phones))):
            data.append([phones[i], emails[i]])

        df = pd.DataFrame(data, columns=["Phone", "Email"])

        output_path = os.path.join(OUTPUT_FOLDER, "result.xlsx")
        df.to_excel(output_path, index=False)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)