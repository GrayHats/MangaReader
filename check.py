#!/usr/bin/env python
'''
inserire i vecchi valori di config.cfg nel database

config.cfg   --> database
'''


from mangadb import store, Manga, Mail


if __name__ == "__main__":

    #verifichiamo
    print '\nVerifica inserimento dati email nel db\n'
    rows = store.find(Mail)
    for row in rows:
        print row.id
        print 'from: %s\nto: %s\nsubject: %s\nsmtp: %s\n'\
                 % (row.from_addr, row.to_addr, row.subject, row.smtp)

    print '\nVerifica inserimento manga nel db\n'
    rows = store.find(Manga)
    for row in rows:
        print 'Manga: %s' % (row.name)
