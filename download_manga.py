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
	manga = y.fetch_title()
	lista = []
	name = y.convert_name(manga) # converte il nome del manga in formato utile per mangareader
	for i in [ '/\d*-\d*-\d*/%s/chapter-\d*.html'  % (name), '/%s/\d\d*'  % (name)	]: # mangareader utiliza entrambe le espressioni regolari ^_^
		for y_link in  y.fetch_links(str(i)): # scorre la lista dei link trovati
			lista.append(y.build_name(str(y_link)))
	for chapter in lista:
		download_chapter(chapter)
			


