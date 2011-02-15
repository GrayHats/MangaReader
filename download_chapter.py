#!/usr/bin/python
''' 
scarica manga
'''

from mangareader import mangareader
from mangareader import download_chapter
from mangareader import download_img
import sys

if __name__ == "__main__":
	if len(sys.argv) == 1 :
		url = raw_input('Inserisci l\'url ... ')
	else:
		url = sys.argv[1]
	download_chapter(url)
			


