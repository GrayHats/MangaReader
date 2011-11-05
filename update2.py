#!/usr/bin/env python
'''
inserire i vecchi valori di config.cfg nel database

config.cfg   --> database
'''


from mangareader import store, Manga, Mail, Chapter
import re

def convert_name(manga):
    return manga.replace("'","")\
            .replace(' - ',' ')\
            .replace(' ','-')\
            .replace('!','')\
            .replace(':','')\
            .lower()

if __name__ == "__main__":
    # Se presenti, linka i capitoli scaricati ai rispettivi manga
    mangas = store.find(Manga)
    for manga in mangas:
        manga_name =unicode('%' + convert_name(manga.name) + '%')
        try: 
            chapters = store.find(Chapter, Chapter.link.like(manga_name))
            for chapter in chapters:
                if not chapter.id_manga: 
                    chapter.id_manga = manga.id
                    print ' set id_manga: %s (%s)' % (manga.id, manga.name)
        except: 
            print 'problemi con %s' % manga_name
            exit(1)

    store.commit()
    # check
    chapters = store.find(Chapter)
    for chapter in chapters:
        if not chapter.id_manga:
            print 'capitolo non associato: %s' % chapter.link
