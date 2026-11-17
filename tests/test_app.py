import tempfile
import unittest
from pathlib import Path

from app import add_note, load_notes


class StorageTests(unittest.TestCase):
    def test_empty_storage(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(load_notes(Path(directory) / "notes.json"), [])

    def test_add_and_read_note(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "notes.json"
            self.assertEqual(add_note("test", path), {"id": 1, "text": "test"})
            self.assertEqual(load_notes(path), [{"id": 1, "text": "test"}])


if __name__ == "__main__":
    unittest.main()
