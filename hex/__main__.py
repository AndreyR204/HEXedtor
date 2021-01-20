import editor
import curses
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', help='path to file', required=True)
    args = parser.parse_args()
    bedit = editor.bin_editor(args.file)
    curses.wrapper(bedit.main)

