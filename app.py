from flask import Flask, request, jsonify
import pdfplumber

app = Flask(__name__)

@app.route('/extract_text', methods=['POST'])
def extract_text():
    if 'pdf' not in request.files:
        return jsonify({"error": "No PDF file uploaded"}), 400
    
    pdf_file = request.files['pdf']
    
    extracted_text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            extracted_text += page.extract_text() + "\n"
    
    return jsonify({"extracted_text": extracted_text.strip()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
