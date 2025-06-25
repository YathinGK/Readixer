from flask import Flask, request, send_file
import os
from summarizer import extract_text_from_pdf, extractive_summary, save_summary_as_pdf

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/summarize', methods=['POST'])
def summarize():
    file = request.files['file']
    if not file:
        return {"error": "No file uploaded"}, 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    text = extract_text_from_pdf(filepath)
    summary = extractive_summary(text, max_sentences=7)
    
    output_path = os.path.join("outputs", f"summary_{file.filename}.pdf")
    os.makedirs("outputs", exist_ok=True)
    save_summary_as_pdf(summary, output_path)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
