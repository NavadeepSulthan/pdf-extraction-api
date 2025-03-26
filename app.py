from flask import Flask, request, jsonify
import pdfplumber
from transformers import pipeline

app = Flask(__name__)

# Load the summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.route('/summarize', methods=['POST'])
def summarize_pdf():
    if 'pdf' not in request.files:
        return jsonify({"error": "No PDF file uploaded"}), 400
    
    pdf_file = request.files['pdf']
    
    extracted_text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
    
    if not extracted_text.strip():
        return jsonify({"error": "No text found in PDF"}), 400

    # Summarize extracted text
    try:
        summary = summarizer(extracted_text, max_length=500, min_length=100, do_sample=False)
        summarized_text = summary[0]['summary_text']
    except Exception as e:
        summarized_text = "Error in summarization: " + str(e)

    return jsonify({"summary": summarized_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
