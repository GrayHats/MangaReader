#!/usr/bin/python
''' 
scarica manga

versione experimental
sto sperimentando l'uso di argparse
'''

from mangareader import mangareader
from mangareader import download_chapter
from mangareader import download_img
from mangareader import stampa
import argparse

from sys import exit 


def download_manga(url):
    y = mangareader(url)
    manga = y.fetch_title_manga()
    name = y.convert_name(manga) # converte il nome del manga in formato utile per mangareader
    lista = y.fetch_chapters_manga(name)
    if not lista:
        stampa('Nessun capitolo trovato')
        exit(-1)
    lista.sort() # basic sort..
    stampa('Elenco capitoli trovati:')
    for chapter in lista:
        stampa('-> %s' % chapter)
    ### for try demo only
    stampa('fine demo')
    exit(1)
    ##
    stampa('\nInizio a scaricare i capitoli')
    for chapter in lista:
        stampa('Scarico capitolo: %s ' % chapter)
        download_chapter(chapter)



if __name__ == "__main__":
#    if len(sys.argv) == 1 :
#        url = raw_input('Inserisci l\'url ... ')
#    else:
#        url = sys.argv[1]
#    download_manga(url)
    parser = argparse.ArgumentParser(description='Download a manga from given\
    url')
    parser.add_argument('url', help='manga url', nargs='+')
    parser.add_argument('-c', '--chapter', help='only chapters from X to\
            Y', nargs=1, metavar='X-Y')
    parser.add_argument('--version', '-v', action='version', version='%(prog)s\
    experimental')
    args = parser.parse_args()
    stampa('argomenti %s' % args)
    if args.chapter:
        x,y = args.chapter[0].split('-')
        print x,y
    stampa('---')
    stampa('Queue: ')
    for url in args.url:
        stampa(' -> %s' % url)
    stampa('---')
    for url in args.url:
        stampa('Download: %s' % url)
        download_manga(url)
