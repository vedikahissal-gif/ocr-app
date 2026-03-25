@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded ❌"

        file = request.files["file"]

        if file.filename == "":
            return "No file selected ❌"

        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        text = ocr_api(path)

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