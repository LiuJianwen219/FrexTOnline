import io
import os

from chardet.enums import LanguageFilter
from chardet.universaldetector import UniversalDetector

def reading_unknown_encoding_file(filename):
    detector = UniversalDetector(LanguageFilter.CHINESE)
    with open(filename, 'rb') as f:
        detector.feed(f.read())
        detector.close()
        encoding = detector.result['encoding']
        f = io.TextIOWrapper(f, encoding=encoding)
        f.seek(0)
        print(f.read())

if __name__ == "__main__":
    reading_unknown_encoding_file("test.py")