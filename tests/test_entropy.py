import tempfile
import unittest
from pathlib import Path

from core.entropy import compute_entropy


class EntropyTests(unittest.TestCase):
    def test_repeated_byte_has_low_entropy(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "low.bin"
            path.write_bytes(b"A" * 4096)
            result = compute_entropy(str(path))

        self.assertEqual(result.entropy, 0.0)
        self.assertFalse(result.is_high_entropy)

    def test_uniform_byte_distribution_has_high_entropy(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "high.bin"
            path.write_bytes(bytes(range(256)) * 32)
            result = compute_entropy(str(path))

        self.assertEqual(result.entropy, 8.0)
        self.assertTrue(result.is_high_entropy)


if __name__ == "__main__":
    unittest.main()
