import spacy
import heapq
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import PyPDF2
from fpdf import FPDF
import os
import re
from difflib import SequenceMatcher

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Function to extract raw text from PDF
def extract_text_from_pdf(pdf_path):
    reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text

# Helper to check sentence similarity
def is_similar(a, b, threshold=0.9):
    return SequenceMatcher(None, a, b).ratio() > threshold

# Extractive summary using TF-IDF
def extractive_summary(text, max_sentences=25, topic=None):
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 20]

    if topic:
        topic = topic.lower()
        topic_sentences = [s for s in sentences if topic in s.lower()]
        if len(topic_sentences) >= 3:
            sentences = topic_sentences[:max_sentences]

    if len(sentences) <= max_sentences:
        return sentences

    cleaned_sentences = []
    for sent in sentences:
        sent_clean = re.sub(r"^\d+[\.\-\)]?\s*", "", sent)
        tokens = [token.text.lower() for token in nlp(sent_clean)
                  if not token.is_stop and not token.is_punct]
        cleaned_sentences.append(" ".join(tokens))

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english', min_df=1)
    tfidf_matrix = vectorizer.fit_transform(cleaned_sentences)

    scores = tfidf_matrix.sum(axis=1)
    scored_sentences = [(score.item(), s) for score, s in zip(scores, sentences)]
    top_sentences = sorted(
        sorted(scored_sentences, key=lambda x: -x[0])[:max_sentences + 3],
        key=lambda x: sentences.index(x[1])
    )

    unique = []
    for _, s in top_sentences:
        if all(not is_similar(s, prev) for prev in unique):
            unique.append(s)

    if len(unique) < 3:
        unique = [s.text.strip() for s in nlp(text).sents if len(s.text.strip()) > 20][:5]

    return unique[:max_sentences]


# Save summary to PDF
def save_summary_as_pdf(summary_lines, output_path="summary_output.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(64, 0, 128)
    pdf.cell(0, 10, "Summary", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(50, 50, 50)

    for line in summary_lines:
        safe_line = line.encode("latin-1", "ignore").decode("latin-1")
        pdf.multi_cell(0, 10, f"- {safe_line}", align="L")
        pdf.ln(1)

    pdf.output(output_path)
    return output_path

# Run script
if __name__ == "__main__":
    pdf_path = input("Enter path to PDF file: ").strip()
    if not os.path.exists(pdf_path):
        print("❌ File not found.")
        exit()

    text = extract_text_from_pdf(pdf_path)
    if not text.strip():
        print("❌ Failed to extract any text.")
        exit()

    summary = extractive_summary(text, max_sentences=7)

    output_file = "summary_" + os.path.splitext(os.path.basename(pdf_path))[0] + ".pdf"
    final_path = save_summary_as_pdf(summary, output_file)
    print(f"\n✅ Summary PDF saved as: {final_path}")
