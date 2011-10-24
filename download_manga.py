#!/usr/bin/python
'''
scarica manga

versione experimental
sto sperimentando l'uso di argparse
'''

from mangareader import mangareader
from mangareader import download_chapter
#from mangareader import download_img
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

def allowed_chapter(numbers):
    '''
        check chapter
    '''
    try:
        chapter_start, chapter_end = numbers.split('-')
        chapter_start = int(chapter_start)
        chapter_end = int(chapter_end)
        if chapter_start > chapter_end or chapter_start < 0:
            raise argparse.ArgumentTypeError('invalid chapters')
        return [chapter_start, chapter_end]
    except:
        raise argparse.ArgumentTypeError('invalid chapters')



def main():
    '''
    the main!
    '''
    parser = argparse.ArgumentParser(description='Download a manga from given\
            url')
    parser.add_argument('url', help='manga url', nargs='+')
    parser.add_argument('-c', '--chapters', help='only chapters from X to\
            Y (integers)' , nargs=1, metavar='X-Y', type=allowed_chapter)
    parser.add_argument('--version', '-v', action='version', version='%(prog)s\
            experimental')
    args = parser.parse_args()
    stampa('argomenti %s' % args)
    stampa('---')
    stampa('Queue: ')
    for url in args.url:
        stampa(' -> %s' % url)
    stampa('---')
    exit(1)
    for url in args.url:
        stampa('Download: %s' % url)
        download_manga(url)




if __name__ == "__main__":
#    if len(sys.argv) == 1 :
#        url = raw_input('Inserisci l\'url ... ')
#    else:
#        url = sys.argv[1]
#    download_manga(url)
    main()
