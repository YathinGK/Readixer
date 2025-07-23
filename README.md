# ✍️ Handwritten Notes Converter & Summary Generator – "Readixer"

A component of **Readixer**, this project focuses on converting handwritten notes into digital text using OCR (Optical Character Recognition) and deep learning models. It provides an intuitive interface for uploading handwritten files and receiving clean, editable text output.

---

## 🚀 Features

- 🖼️ Upload handwritten images or PDF files
- 🧠 Utilizes a trained OCR model for handwriting recognition
- 📝 Extracts readable and editable digital text
- 📦 API integration support for external use
- 🌐 Clean and interactive UI built with Streamlit
Summary Generator
- 📝 Paste or Upload Your Notes
- ⚡ Generate concise summaries instantly
- 🧠 Built using Natural Language Processing techniques
- 🔍 Supports keyword-based or custom-length summarization
---

## 🧰 Tech Stack

🛠️ Tech Stack

🖼️ Handwritten Notes to Digital Text

- Frontend/UI:
  • React for the Frontenr

- Backend:
  • Python – powering logic, image processing, and OCR pipeline

- OCR Model:
  • Trained using TensorFlow/Keras (e.g., CNN for handwriting recognition)

- Libraries Used:
  • opencv-python – for image processing and pre-processing
  • pytesseract – wrapper for Google’s Tesseract OCR engine
  • Pillow (PIL) – for handling and manipulating images
  • numpy – numerical operations and array management
  • streamlit – UI interaction and file upload
  • tensorflow / keras – for model inference (if custom model is used)

🧠 Summary Generator

- Frontend/UI:
  • Streamlit – same unified interface as OCR component

- Backend:
  • Python – for NLP processing and summarization logic

- NLP Techniques/Models:
  • Extractive summarization using NLP algorithms
  • Libraries like spaCy or NLTK (for text processing)
  • Transformers (if using models like BERT, T5 or Pegasus)
---

## 🖼️ How It Works

1. Upload an image or scanned file of handwritten notes.
2. The backend processes the image using preprocessing (grayscale, thresholding, etc.).
3. The model predicts the characters and words.
4. The result is displayed as editable text for further usage.

HomePage
![image](https://github.com/user-attachments/assets/12afc84f-c65b-4568-b85e-69ddd0df7805)

Handwritting Conversion
![image](https://github.com/user-attachments/assets/df94981d-0bc2-4178-9d89-0fa0df4ccb70)

Summary Generator 
![image](https://github.com/user-attachments/assets/bf82748d-dff4-4231-9ad5-a35b470ef2e0)




