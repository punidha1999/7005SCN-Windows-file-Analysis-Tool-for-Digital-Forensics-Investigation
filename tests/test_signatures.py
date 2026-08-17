import tempfile
import unittest
from pathlib import Path

from core.signatures import analyze_signature


class SignatureTests(unittest.TestCase):
    def test_pdf_signature_matches_pdf_extension(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.pdf"
            path.write_bytes(b"%PDF-1.7\nexample")
            result = analyze_signature(str(path))

        self.assertIn(".pdf", result.detected_exts)
        self.assertFalse(result.mismatch)

    def test_pdf_signature_flags_false_txt_extension(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.txt"
            path.write_bytes(b"%PDF-1.7\nexample")
            result = analyze_signature(str(path))

        self.assertIn(".pdf", result.detected_exts)
        self.assertTrue(result.mismatch)


if __name__ == "__main__":
    unittest.main()
