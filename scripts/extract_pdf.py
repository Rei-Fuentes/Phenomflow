from pypdf import PdfReader
import sys

def extract_text(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading {pdf_path}: {str(e)}"

files = [
    "/Users/reinerfuentesferrada/ONLINE_DS_THEBRIDGE_Rei/PhenomFlow/paper reference/fpsyg-16-1522701.pdf",
    "/Users/reinerfuentesferrada/ONLINE_DS_THEBRIDGE_Rei/PhenomFlow/paper reference/fpsyg-16-1570124.pdf"
]

for f in files:
    print(f"--- START OF {f} ---")
    print(extract_text(f))
    print(f"--- END OF {f} ---")
