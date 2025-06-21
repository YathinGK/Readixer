from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import base64
import cv2
from google.cloud import vision
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ✅ Securely decode base64 credentials and store temporarily
if 'GOOGLE_CREDENTIALS_BASE64' in os.environ:
    decoded = base64.b64decode(os.environ['GOOGLE_CREDENTIALS_BASE64'])
    with open("google_credentials.json", "w") as f:
        f.write(decoded.decode())
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "google_credentials.json"
else:
    raise EnvironmentError("Missing GOOGLE_CREDENTIALS_BASE64 environment variable")

# Register custom font
pdfmetrics.registerFont(TTFont('Times-Roman', 'times.ttf'))

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    output_path = "processed_image.png"
    cv2.imwrite(output_path, thresh)
    return output_path

def recognize_text(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    if response.error.message:
        raise Exception(f"Google Vision API error: {response.error.message}")

    return response.full_text_annotation.text or "No text detected."

def generate_pdf(text, output_path='handwritten_output.pdf'):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name='Title',
        fontName='Times-Roman',
        fontSize=18,
        leading=22,
        alignment=1,
        spaceAfter=12
    )

    body_style = ParagraphStyle(
        name='Body',
        fontName='Times-Roman',
        fontSize=12,
        leading=16,
        alignment=TA_JUSTIFY,
        spaceAfter=12
    )

    story = []
    story.append(Paragraph("Handwritten Notes to Digital Text", title_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", body_style))
    story.append(Spacer(1, 0.2 * inch))

    for para in text.strip().split('\n'):
        if para.strip():
            story.append(Paragraph(para.strip(), body_style))

    doc.build(story)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        input_path = 'input_image.png'
        file.save(input_path)

        preprocessed_path = preprocess_image(input_path)
        extracted_text = recognize_text(preprocessed_path)
        generate_pdf(extracted_text)

        # Clean up temporary files
        os.remove(preprocessed_path)
        os.remove(input_path)

        return send_file('handwritten_output.pdf', as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
