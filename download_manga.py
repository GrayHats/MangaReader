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
	y = mangareader(url)
	manga = y.fetch_title_manga()
	name = y.convert_name(manga) # converte il nome del manga in formato utile per mangareader
	lista = y.fetch_chapters_manga(name)
	lista.sort() # basic sort..
	for chapter in lista:
		download_chapter(chapter)
			


