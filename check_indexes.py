from pathlib import Path
data = Path("web_app.py").read_text(encoding="utf-8")
print("start index of download route:", data.find("@app.route('/docs/<path:filename>')"))
print("start index of pdf function:", data.find("def generate_pdf_from_html"))

