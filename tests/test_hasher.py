import hashlib
import tempfile
import unittest
from pathlib import Path

from core.hasher import compute_hashes, find_duplicates, load_hashset, match_against_hashset


class HasherTests(unittest.TestCase):
    def test_compute_hashes_matches_hashlib(self):
        payload = b"ForensiScan deterministic hashing test"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.bin"
            path.write_bytes(payload)
            result = compute_hashes(str(path))

        self.assertEqual(result.md5, hashlib.md5(payload).hexdigest())
        self.assertEqual(result.sha1, hashlib.sha1(payload).hexdigest())
        self.assertEqual(result.sha256, hashlib.sha256(payload).hexdigest())
        self.assertEqual(result.size, len(payload))

    def test_duplicate_and_hashset_matching(self):
        payload = b"duplicate content"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = root / "one.bin"
            second = root / "two.bin"
            first.write_bytes(payload)
            second.write_bytes(payload)

            hashes = [compute_hashes(str(first)), compute_hashes(str(second))]
            duplicates = find_duplicates(hashes)

            hashset_file = root / "known.txt"
            hashset_file.write_text(hashes[0].sha256 + "\n", encoding="utf-8")
            known = load_hashset(str(hashset_file))
            matches = match_against_hashset(hashes, known)

        self.assertEqual(len(duplicates), 1)
        self.assertEqual(len(next(iter(duplicates.values()))), 2)
        self.assertEqual(len(matches), 2)


if __name__ == "__main__":
    unittest.main()
