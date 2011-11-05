#!/usr/bin/env python
'''
agenda
work in progress
'''

from mangareader import store, Chapter, Manga


def uscita():
    '''
        simply exit function
    '''
    print 'Uscita..'
    exit(1)

def add_manganame():
    '''
        add manga from name
    '''
    print "\n\nINSERIMENTO NUOVO MANGA\n"
    manga = store.add(Manga())
    manga.name = unicode(raw_input('Nome Manga: '))
    conferma = raw_input("(q per annullare): ")
    if conferma == "q":
        return
    store.commit()
    print '%s inserito' % manga.name
    return

def delete_chapter():
    '''
        remove event
    '''
    record_id = int(raw_input('ID da rimuovere: '))
    record = store.find(Chapter, Chapter.id == record_id)
    if not record.count():
        print 'nessun evento da cancellare'
        return
    for i in record.order_by(Chapter.id):
        print "%s - %s - status; %s" % (i.id, i.link,\
                i.status)

    conferma = raw_input("(q per annullare): ")
    if conferma == "q":
        print 'operazione annullata'
        return
    print 'evento cancellato'
    store.remove(record[0])
    store.commit()
    return


def delete_manga():
    '''
        remove event
    '''
    record_id = int(raw_input('ID da rimuovere: '))
    record = store.find(Manga, Manga.id == record_id)
    if not record.count():
        print 'nessun evento da cancellare'
        return
    for i in record.order_by(Manga.id):
        print "%s - %s - status; %s" % (i.id, i.name,\
                i.status)

    conferma = raw_input("(q per annullare): ")
    if conferma == "q":
        print 'operazione annullata'
        return
    store.remove(record[0])
    store.commit()
    print 'evento cancellato'
    return


def cerca():
    '''
        search record
    '''
    print 'non implementato'

def manga_list():
    '''
        print manga list
    '''
    mangas = store.find(Manga)
    for manga in mangas.order_by(Manga.name):
        chapters = store.find(Chapter, Chapter.id_manga == manga.id)
        print '%s (%s)\t\t\t - scaricati: %s'\
                 % (manga.name, manga.id, chapters.count())

def status_zero():
    '''
    '''
    print "\n\nLista chapter da scaricare!\n"
    chapters = store.find(Chapter, Chapter.status == 0)
    for chapter in chapters.order_by(Chapter.id):
        print "%s - %s" % (chapter.id, chapter.link)

def menu(opzioni):
    '''
        a simply menu
    '''
    while 1:
        print '\n\n Scelte Possobili:'
        for opzione in sorted(opzioni.items(), key=lambda (k, v): (v, k)):
            # opzione == ('key', (value, <function>, 'descr'))
            print '  %s - %s' % (opzione[0], opzione[1][2])
        try:
            scelta = raw_input('\nChe fai? -> ').lower()
        except EOFError:
            print "\n\n Oook, bye."
            break
        try:
            opzioni[scelta][1]()
        except KeyError:
            return

def main():
    '''
     the main function ^_^
    '''
    opzioni = {
            'a':(5, add_manganame,'aggiungi manga'),
            'm':(10, manga_list,'lista manga'),
            'z':(90, status_zero,'lista capitoli con status zero'),
            'rc':(95, delete_chapter,'elimina un capitolo'),
            'rm':(95, delete_manga,'elimina un manga'),
            'q':(100, uscita, 'esci')
            }
    #import pdb
    #pdb.set_trace()
    menu(opzioni)

if __name__ == '__main__':
    while True:
        main()
