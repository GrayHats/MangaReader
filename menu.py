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
    print 'quitting..'
    exit(1)

def add_manganame():
    '''
        add manga from name
    '''
    print "\n\nADD NEW MANGA\n"
    manga = store.add(Manga())
    manga.name = unicode(raw_input('Manga Name: '))
    conferma = raw_input("(q to abort): ")
    if conferma == "q":
        return
    store.commit()
    print '%s added' % manga.name
    return

def delete_chapter():
    '''
        remove event
    '''
    record_id = int(raw_input('ID to been removed: '))
    record = store.find(Chapter, Chapter.id == record_id)
    if not record.count():
        print 'nothing to remove'
        return
    for i in record.order_by(Chapter.id):
        print "%s - %s - status; %s" % (i.id, i.link,\
                i.status)

    conferma = raw_input("(q to abort): ")
    if conferma == "q":
        print 'aborted'
        return
    print 'record removed'
    store.remove(record[0])
    store.commit()
    return


def delete_manga():
    '''
        remove event
    '''
    record_id = int(raw_input('ID to been removed: '))
    record = store.find(Manga, Manga.id == record_id)
    if not record.count():
        print 'nothing to remove'
        return
    for i in record.order_by(Manga.id):
        print "%s - %s - status; %s" % (i.id, i.name,\
                i.status)

    conferma = raw_input("(q to abort): ")
    if conferma == "q":
        print 'aborted'
        return
    store.remove(record[0])
    store.commit()
    print 'record removed'
    return


def cerca():
    '''
        search record
    '''
    manga_id = int(raw_input('ID  manga: '))
    manga = store.find(Manga, Manga.id == manga_id).one()
    chapters = store.find(Chapter, Chapter.id_manga == manga_id)
    print '%s - %s' % (manga.name, manga.data)
    for chapter in chapters:
        print ''
        print '%s - %s' % (chapter.link, chapter.data)



def manga_list():
    '''
        print manga list
    '''
    mangas = store.find(Manga)
    for manga in mangas.order_by(Manga.name):
        chapters = store.find(Chapter, Chapter.id_manga == manga.id)
        print '%s (id:%s)\t\t\t - scaricati: %s'\
                 % (manga.name, manga.id, chapters.count())

def manga_list_recentlydownloaded():
    pass


def manga_list_download_history():
    from datetime import timedelta, datetime, date
    now = datetime.now()
    today = date.today()
    mangas = store.find(Manga, Manga.data < now )
    for manga in mangas.order_by(Manga.data):
        print "%s %s -> %s" % (manga.name, manga.data.date(),
                        (today - manga.data.date()).days )



def manga_list_missed_manga():
    '''
        manga con 0 capitoli scaricati
    '''
    mangas = store.find(Manga)
    for manga in mangas.order_by(Manga.name):
        chapters = store.find(Chapter, Chapter.id_manga == manga.id)
        if chapters.count() == 0:
            print '%s (id:%s)' % (manga.name, manga.id)

def status_zero():
    '''
    '''
    print "\n\nList chapters still to download!\n"
    chapters = store.find(Chapter, Chapter.status == 0)
    for chapter in chapters.order_by(Chapter.id):
        print "%s - %s" % (chapter.id, chapter.link)

def menu(opzioni):
    '''
        a simply menu
    '''
    while 1:
        print '\n\n Menu:'
        for opzione in sorted(opzioni.items(), key=lambda (k, v): (v, k)):
            # opzione == ('key', (value, <function>, 'descr'))
            print '  %s - %s' % (opzione[0], opzione[1][2])
        try:
            scelta = raw_input('\nso, what? -> ').lower()
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
            'a':(5, add_manganame,'add manga'),
            'l':(10, manga_list,'list manga'),
            #'lr':(11, manga_list_recentlydownloaded,'lista manga scaricati recentemente'),
            'lm':(12, manga_list_missed_manga,'list manga never downloaded'),
            'lh':(12, manga_list_download_history,\
                    'list history downloaded manga'),
            'd':(10, cerca,'detail  manga'),
            'z':(90, status_zero,'list chapter to download'),
            'rc':(95, delete_chapter,'remove a chapter from db'),
            'rm':(95, delete_manga,'remove a manga from db'),
            'q':(100, uscita, 'quit')
            }
    #import pdb
    #pdb.set_trace()
    menu(opzioni)

if __name__ == '__main__':
    while True:
        main()
