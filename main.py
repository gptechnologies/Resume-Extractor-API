from flask import Flask, request, jsonify
import pdfplumber
import requests
from io import BytesIO

app = Flask(__name__)

@app.route("/extract-pdf-text", methods=["POST"])
def extract_pdf_text():
    data = request.json
    pdf_url = data.get("pdf_url")

    if not pdf_url:
        return jsonify({"error": "Missing 'pdf_url' field"}), 400

    try:
        # Download the PDF
        response = requests.get(pdf_url)
        response.raise_for_status()

        # Extract text
        with pdfplumber.open(BytesIO(response.content)) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)

        return jsonify({"text": text.strip()})

    except Exception as e:
        print("🚨 ERROR:", str(e))  # This will show in Render logs
        return jsonify({"error": str(e)}), 500
