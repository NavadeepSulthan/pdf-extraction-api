from flask import Flask, request, jsonify
import pdfplumber
from transformers import pipeline

app = Flask(__name__)

# Load the summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.route('/extract_text', methods=['POST'])
def extract_text():
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

    # Summarize extracted text (if too long, break into chunks)
    max_length = 5000  # Adjust based on need
    min_length = 100
    try:
        summary = summarizer(extracted_text, max_length=max_length, min_length=min_length, do_sample=False)
        summarized_text = summary[0]['summary_text']
    except Exception as e:
        summarized_text = "Error in summarization: " + str(e)

    return jsonify({
        "extracted_text": extracted_text.strip(),
        "summary": summarized_text
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
