import re
import hashlib
from bs4 import BeautifulSoup
from langdetect import detect

class ArticleProcessor:
    def clean_html(self, html_content):
        if not html_content:
            return ""
        soup = BeautifulSoup(html_content, "html.parser")
        return soup.get_text(separator=' ', strip=True)

    def normalize_text(self, text):
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def detect_language(self, text):
        try:
            return detect(text)
        except:
            return "unknown"

    def generate_hash(self, text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def chunk_text(self, text, chunk_size=500):
        words = text.split()
        return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
