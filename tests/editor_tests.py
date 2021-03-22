import unittest
import curses
from hex import editor


class TestStringMethods(unittest.TestCase):

    def test_filepath(self):
        bedit = editor.BinEditor("../hex/__main__.py")
        curses.wrapper(bedit.main)
        self.assertEqual(bedit.filepath, "../hex/__main__.py")

    def test_max_byte(self):
        bedit = editor.BinEditor("../hex/__main__.py")
        curses.wrapper(bedit.main)
        self.assertEqual(bedit.max_byte_count, 32)

    def test_read_data(self):
        self.assertEqual(editor.read_data("../hex/__main__.py"), [105, 109, 112, 111, 114, 116, 32, 101, 100, 105, 116, 111, 114, 13, 10, 105, 109, 112, 111, 114, 116, 32, 99, 117, 114, 115, 101, 115, 13, 10, 105, 109, 112, 111, 114, 116, 32, 97, 114, 103, 112, 97, 114, 115, 101, 13, 10, 13, 10, 105, 102, 32, 95, 95, 110, 97, 109, 101, 95, 95, 32, 61, 61, 32, 39, 95, 95, 109, 97, 105, 110, 95, 95, 39, 58, 13, 10, 32, 32, 32, 32, 112, 97, 114, 115, 101, 114, 32, 61, 32, 97, 114, 103, 112, 97, 114, 115, 101, 46, 65, 114, 103, 117, 109, 101, 110, 116, 80, 97, 114, 115, 101, 114, 40, 41, 13, 10, 32, 32, 32, 32, 112, 97, 114, 115, 101, 114, 46, 97, 100, 100, 95, 97, 114, 103, 117, 109, 101, 110, 116, 40, 39, 45, 45, 102, 105, 108, 101, 39, 44, 32, 39, 45, 102, 39, 44, 32, 104, 101, 108, 112, 61, 39, 112, 97, 116, 104, 32, 116, 111, 32, 102, 105, 108, 101, 39, 44, 32, 114, 101, 113, 117, 105, 114, 101, 100, 61, 84, 114, 117, 101, 41, 13, 10, 32, 32, 32, 32, 97, 114, 103, 115, 32, 61, 32, 112, 97, 114, 115, 101, 114, 46, 112, 97, 114, 115, 101, 95, 97, 114, 103, 115, 40, 41, 13, 10, 32, 32, 32, 32, 98, 101, 100, 105, 116, 32, 61, 32, 101, 100, 105, 116, 111, 114, 46, 66, 105, 110, 69, 100, 105, 116, 111, 114, 40, 97, 114, 103, 115, 46, 102, 105, 108, 101, 41, 13, 10, 32, 32, 32, 32, 99, 117, 114, 115, 101, 115, 46, 119, 114, 97, 112, 112, 101, 114, 40, 98, 101, 100, 105, 116, 46, 109, 97, 105, 110, 41, 13, 10])

    def test_max_byte(self):
        self.assertEqual(editor.read_file("../hex/__main__.py"), b"import editor\r\nimport curses\r\nimport argparse\r\n\r\nif __name__ == '__main__':\r\n    parser = argparse.ArgumentParser()\r\n    parser.add_argument('--file', '-f', help='path to file', required=True)\r\n    args = parser.parse_args()\r\n    bedit = editor.BinEditor(args.file)\r\n    curses.wrapper(bedit.main)\r\n")


if __name__ == '__main__':
    unittest.main()