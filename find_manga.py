#!/usr/bin/env python
'''
fetch new chapters from http://www.mangareader.net/latest,
download and report by mail
'''
from mangareader import mangareader
from mangareader import stampa
import argparse


def options():
    parser = argparse.ArgumentParser(description = '''
    temp
    '''
    )
    parser.add_argument("name", help = 'nome manga')
    return parser.parse_args()


if __name__ == "__main__":
    args = options()
    # fetch new links from website

    x = mangareader('http://www.mangareader.net/alphabetical')
    name = x.convert_name(args.name)
    link = x.find_manga(name)
    print link
