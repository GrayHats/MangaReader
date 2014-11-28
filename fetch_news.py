#!/usr/bin/env python
'''
fetch new chapters from http://www.mangareader.net/latest,
download and report by mail
'''
from mangareader import mangareader
from mangareader import stampa
from mangareader import download_chapter
from mangadb import store, Manga, Chapter, Mail
from datetime import datetime


def now():
    return datetime.now()


def send_mail(body):
    import smtplib
    rows = store.find(Mail)
    for row in rows:
        body2 = "From: %s\n" % (row.from_addr)
        body2 += "To: %s\n" % (row.to_addr)
        body2 += "Subject: %s\n\n" % (row.subject,)
        body2 += body
        server = smtplib.SMTP(row.smtp)
        server.sendmail(row.from_addr, [row.to_addr], body2)
        server.quit()


def main():
    body = ''

    # fetch new links from website
    x = mangareader('http://www.mangareader.net/latest')
    for manga in store.find(Manga):
        name = x.convert_name(manga.name)
        links = x.fetch_chapters_manga(name)
        if links:
            for link, number in links:
                if not store.find(Chapter.link,
                                  Chapter.link == unicode(link)).count():
                    new_chapter = store.add(Chapter())
                    new_chapter.link = unicode(link)
                    new_chapter.status = 0
                    new_chapter.id_manga = manga.id
                    store.add(new_chapter)
                    store.commit()
                    store.flush()

    # download links with status 0
    rows = store.find(Chapter, Chapter.status == 0)
    if rows.count():
        stampa('Da Scaricare:')
        for row in rows:
            stampa(' %s' % row.link)
        for row in rows:
            # re-check status, just in case..
            this_chap = store.find(Chapter, Chapter.id == row.id)
            if this_chap[0].status == 2:
                stampa('Status cambiato per %s' % row.link)
                continue
            row.status = 2
            row.data = now()
            store.commit()
            store.flush()
            ##
            stampa('\nScarico %s' % row.link)
            if download_chapter(row.link):
                row.status = 1
                row.data = now()
                row.manga.data = now()
                store.commit()
                store.flush()
                body += '\nScaricato %s:\n' % (row.link)
            else:
                body += '\nErrore nello scaricare %s:\n' % (row.link)

    # report links with status 0
    rows = store.find(Chapter, Chapter.status == 0)
    if rows.count():
        body += '\n\n###Da scaricare'
        for row in rows:
            body += '\nDa scaricare %s:\n' % (row.link)
    # report links with status 2
    rows = store.find(Chapter, Chapter.status == 2)
    if rows.count():
        body += '\n\n###Chapter in via di scaricamento'
        for row in rows:
            body += '\n  --> %s:\n' % (row.link)
    if body:
        send_mail(body)


if __name__ == "__main__":
    main()
