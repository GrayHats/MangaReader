#!/usr/bin/python
''' 
scarica manga
'''

from mangareader import mangareader
from mangareader import download_chapter
from mangareader import stampa
import argparse


def options():
    parser = argparse.ArgumentParser(description = '''
    Scarica un manga da mangareader.net
    '''
    )
    parser.add_argument("url", help = 'url della pagina principale del manga')
    parser.add_argument("-f", '--from_chapter', help = 'inizia dal capitolo X',
            default = 0, type = int)
    parser.add_argument("-t", '--to_chapter', help = 'finisce al capitolo  Y',
            default = 0, type = int)
    return parser.parse_args()

def check_chapter_number(args, number):
    if (args.from_chapter and args.to_chapter):
        if args.from_chapter <= number <= args.to_chapter:
            return True
        else:
            return False
    if args.from_chapter:
        if args.from_chapter <= number:
            return True
        else:
            return False
    if args.to_chapter:
        if number <= args.to_chapter:
            return True
        else:
            return False
    return True

if __name__ == "__main__":
    args = options()
    print args
    Y = mangareader(args.url)
    MANGA = Y.fetch_title_manga()
    # converte il nome del manga in formato utile per mangareader
    NAME = Y.convert_name(MANGA) 
    LISTA = Y.fetch_chapters_manga(NAME)
    LISTA.sort() # basic sort..
    stampa('Elenco capitoli trovati:')
    for chapter, number in LISTA:
        if check_chapter_number(args, int(number)):
            stampa('-> %s' % chapter)
    stampa('\nInizio a scaricare i capitoli')
    for chapter, number in LISTA:
        if check_chapter_number(args, int(number)):
            stampa('Scarico capitolo: %s ' % chapter)
            download_chapter(chapter)
            


