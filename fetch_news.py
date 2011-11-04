#!/usr/bin/env python

from mangareader import mangareader
from mangareader import stampa
from mangareader import download_chapter
from mangareader import store, Mail, Manga, Chapter
#from mangareader import stampa
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
    for manga in store.find(Manga.name): # scorriamo la lista dei manga
        name = x.convert_name(manga) # converte il nome del manga in formato utile per mangareader
        rows = x.fetch_chapters_manga(name)
        if rows :
            for row in rows:
                links.append(row)
    # check links against db
    for link in links:
        #link_t = (link,)
        if not store.find(Chapter.link, Chapter.link == unicode(link)).count():
            print 'aggiungo %s' % link
            new_chapter = Chapter()
            new_chapter.link = unicode(link)
            new_chapter.status = 0
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
            #if download_chapter(row.link) :
            if 1 == 1 :
                row.status = 1
                row.data = now()
                store.commit()
        #        link_t = (link[0],)
        #        c.execute('''update chapters set status = 1 where link like ?  ''', link_t)
                body += '\nScaricato %s:\n' % (row.link)
            else:
                body += '\nErrore nello scaricare %s:\n' % (row.link)

    # report links with status 0
    rows = store.find(Chapter, Chapter.status == 0)
    if rows.count():
        body += '\n\n###Da scaricare'
        for row in rows:
            body += '\nDa scaricare %s:\n' % (row.link)
    #if body:
    #    send_mail(body, smtp, fromaddr, toaddr,subject)
    print body
