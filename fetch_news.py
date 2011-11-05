#!/usr/bin/env python
'''
fetch new chapters from http://www.mangareader.net/latest,
download and report by mail
'''

from mangareader import mangareader
from mangareader import stampa
from mangareader import download_chapter
from mangareader import store, Mail, Manga, Chapter
from datetime import datetime


def now():
    return datetime.now()

def send_mail(body):
    import smtplib
    rows = store.find(Mail)
    for row in rows:
        body2 = "Subject: %s\n\n" %(row.subject,)
        body2 += body
        server = smtplib.SMTP(row.smtp)
        server.sendmail(row.from_addr, [row.to_addr], body2)
        server.quit()


if __name__ == "__main__":
    body= ''

    # fetch new links from website
    x = mangareader('http://www.mangareader.net/latest')
    links=[]
    for manga in store.find(Manga):
        name = x.convert_name(manga.name)
        links = x.fetch_chapters_manga(name)
        if links :
            for link in links:
                if not store.find(Chapter.link, Chapter.link == unicode(link)).count():
                    new_chapter = store.add(Chapter())
                    new_chapter.link = unicode(link)
                    new_chapter.status = 0
                    new_chapter.id_manga = manga.id
                    store.add(new_chapter)
    store.commit()

    # download links with status 0
    rows = store.find(Chapter, Chapter.status == 0)
    if rows.count():
        stampa('Da Scaricare:')
        for row in rows:
            stampa(' %s' % row.link)
        for row in rows:
            stampa('\nScarico %s' % row.link)
            if download_chapter(row.link) :
                row.status = 1
                row.data = now()
                row.manga.data = now()
                store.commit()
                body += '\nScaricato %s:\n' % (row.link)
            else:
                body += '\nErrore nello scaricare %s:\n' % (row.link)

    # report links with status 0
    rows = store.find(Chapter, Chapter.status == 0)
    if rows.count():
        body += '\n\n###Da scaricare'
        for row in rows:
            body += '\nDa scaricare %s:\n' % (row.link)
    if body:
        send_mail(body)
