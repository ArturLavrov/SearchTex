from markdown_it import MarkdownIt
from pypdf import PdfReader
import io

class File:
    def __init__(self, file_name, file_content):
        self.file_name = file_name
        self.file_content = file_content  # expected to be bytes

    def parse(self):
        if self.file_name.endswith(".pdf"):
            return self._parse_text_from_pdf(self.file_content)
        elif self.file_name.endswith(".md") or self.file_name.endswith(".markdown"):
            return self._parse_text_from_markdown(self.file_content)
        else:
            return {
                "error": f"Unsupported file type: {self.file_name}"
            }

    @staticmethod
    def _parse_text_from_pdf(file_bytes):
        reader = PdfReader(io.BytesIO(file_bytes))
        return "\n".join([page.extract_text() or "" for page in reader.pages])

    @staticmethod
    def _parse_text_from_markdown(file_bytes):
        md = MarkdownIt()
        text = file_bytes.decode("utf-8")
        tokens = md.parse(text)
        return "\n".join([t.content for t in tokens if t.type == "inline"])
