#!/usr/bin/python
'''
scarica manga
'''

from mangareader import download_chapter
import sys

if __name__ == "__main__":
    if len(sys.argv) == 1:
        URL = raw_input('Inserisci l\'url ... ')
    else:
        URL = sys.argv[1]
    download_chapter(URL)
