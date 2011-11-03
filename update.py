#!/usr/bin/env python
'''
inserire i vecchi valori di config.cfg nel database

config.cfg   --> database
'''


from ConfigParser import ConfigParser
from mangareader import store, Manga, Mail
from os import path
from sys import argv


if __name__ == "__main__":
    # import config
    dirname = path.dirname(path.abspath(argv[0]))
    configfile = 'config.cfg'
    config = ConfigParser()
    config.read(path.join(dirname, configfile))
    fromaddr = config.get('mail','fromaddr')
    toaddr = config.get('mail','toaddr')
    subject = config.get('mail','subject')
    smtp = config.get('mail','smtp')
    p = config.get('mangalist','manga_list')
    manga_list = p.replace('\n','').split(',')

    # opzioni per invio email
    mail = Mail()
    mail.from_addr = unicode(fromaddr)
    mail.to_addr = unicode(toaddr)
    mail.subject = unicode(subject)
    mail.smtp = unicode(smtp)
    store.add(mail)
    store.commit()

    # nomi dei manga
    for manga_name in manga_list:
        manga = Manga()
        manga.name = unicode(manga_name)
        store.add(manga)
    store.commit()

