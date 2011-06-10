#!/usr/bin/env python

from mangareader import mangareader
from mangareader import download_chapter
import smtplib
import sys, os
from pysqlite2 import dbapi2 as sqlite3
from ConfigParser import ConfigParser


def send_mail(body, fromaddr, toaddr, subject):
	body2 = "Subject: %s\n\n" %(subject,)
	body2 += body
	server = smtplib.SMTP('localhost')
	server.sendmail(fromaddr, toaddr, body2)
	server.quit()


if __name__ == "__main__":
	# import config
	dirname = os.path.dirname(os.path.abspath(sys.argv[0]))
	configfile = 'mangareader.cfg'
	config = ConfigParser()
	config.read(os.path.join(dirname, configfile))
	fromaddr = config.get('mail','fromaddr')
	toaddr = [config.get('mail','toaddr')]
	subject = config.get('mail','subject')
	p = config.get('mangalist','manga_list')
	manga_list = p.replace('\n','').split(',')
	# open database
	dirname = os.path.dirname(os.path.abspath(sys.argv[0]))
	database = dirname+'/mangareader.db'
	db = sqlite3.connect(database)
	db.isolation_level = None
	c = db.cursor()

	body= ''				

	# fetch new links from website
	x = mangareader('http://www.mangareader.net/latest')
	links=[]
	for manga in manga_list: # scorriamo la lista dei manga
		name = x.convert_name(manga) # converte il nome del manga in formato utile per mangareader
		rows = x.fetch_chapters_manga(name)
		if rows :
			for row in rows:
				links.append(link)
	# check links against db
	for link in links:
		link_t = (link,)
		c.execute('''SELECT COUNT(id) FROM chapters WHERE link LIKE ?  ''', link_t)
		if not c.fetchone()[0]:
			c.execute('''insert into chapters (link, status) values (?,0) ''',link_t)

	# download links with status 0
	c.execute('''select link from chapters where status = 0 ''')
	links = c.fetchall()
	if not len(links) == 0:
		for link in links:
			if download_chapter(link[0]) :
				link_t = (link[0],)
				c.execute('''update chapters set status = 1 where link like ?  ''', link_t)
				body += '\nScaricato %s:\n' % (link[0])
			else:
				body += '\nErrore nello scaricare %s:\n' % (link)

	# report links with status 0
	c.execute('''select link from chapters where status = 0 ''')
	links = c.fetchall()
	if not len(links) == 0:
		body += '\n\n###Da scaricare'
		for link in links:
				body += '\nDa scaricare %s:\n' % (link[0])
	if body:
		#print body
		send_mail(body,fromaddr, toaddr,subject)
