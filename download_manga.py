#!/usr/bin/python
''' 
scarica manga
'''

from mangareader import mangareader
from mangareader import download_chapter
from mangareader import download_img
from mangareader import stampa

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
	if not lista:
		print 'nessun capitolo trovato'
		print lista
		sys.exit(-1)
	lista.sort() # basic sort..
	stampa('Elenco capitoli trovati:')
	for chapter in lista:
		stampa('-> %s' % chapter)
	stampa('\nInizio a scaricare i capitoli')
	for chapter in lista:
		stampa('Scarico capitolo: %s ' % chapter)
		download_chapter(chapter)
			


