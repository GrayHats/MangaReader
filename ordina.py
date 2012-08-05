#!/usr/bin/env python

from shutil import copy, move
from os import walk, path, mkdir
import argparse

def move_file(src, dest):
    try:
        move(src, dest)
        return
    except:
        print 'unable to move %s' %src

def make_dir(dir):
    try:
        mkdir(dir)
    except OSError as e:
        pass


def parse_dir(dir, ext):
  """
    scansiona la dir in cerca di determinati files
    contenenti ext
    e
    ritorna un array contenente
    [(file,relativopath),]
  """
  files=[]
  for dirname, dirnames, filenames in walk(dir):
    for filename in filenames:
      if ext in filename:
        files.append((filename, path.join(dirname, filename)))
  return files


def options():
    parser = argparse.ArgumentParser(description = '''
    script per ordinare i manga scaricati
    '''
    )
    parser.add_argument("dir_target", 
            help = 'cartella in cui cercare manga')
    parser.add_argument("dir_destination", 
            help = 'cartella in cui spostare i manga catalogati')
    return parser.parse_args()


def main():
    args = options()
    dir_target = args.dir_target
    dir_destination = args.dir_destination
    make_dir(dir_destination)
    mangas = parse_dir(dir_target, '.cbz')
    for manga, mangapath in mangas:
        dirmanga = path.join(dir_destination, manga[:-8]) 
        make_dir(dirmanga)
        move_file(mangapath,dirmanga)

if __name__ == "__main__":
    main()
