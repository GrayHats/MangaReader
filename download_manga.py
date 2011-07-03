#!/usr/bin/python
''' 
scarica manga
'''

from mangareader import mangareader
from mangareader import download_chapter
from mangareader import stampa

import sys


if __name__ == "__main__":
    if len(sys.argv) == 1 :
        URL = raw_input('Inserisci l\'url ... ')
    else:
        URL = sys.argv[1]
    Y = mangareader(URL)
    MANGA = Y.fetch_title_manga()
    # converte il nome del manga in formato utile per mangareader
    NAME = Y.convert_name(MANGA) 
    LISTA = Y.fetch_chapters_manga(NAME)
    LISTA.sort() # basic sort..
    stampa('Elenco capitoli trovati:')
    for chapter in LISTA:
        stampa('-> %s' % chapter)
    stampa('\nInizio a scaricare i capitoli')
    for chapter in LISTA:
        stampa('Scarico capitolo: %s ' % chapter)
        download_chapter(chapter)
            


