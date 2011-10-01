#import urllib2
import urllib
#from BeautifulSoup import BeautifulSoup
import re
import sys, os


dirname = os.path.dirname(os.path.abspath(sys.argv[0]))

def stampa(string):
	sys.stdout.write(string + '\n')

def stampa_err(string):
	sys.stderr.write(string + '\n')
	from datetime import datetime
	now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
	file = os.path.join(dirname,'log_error')
	log = open(file, 'a')
	log.write('%s: %s%s' %(now, string, '\n'))
	log.close()

class logfile:
	def __init__(self, logfile):
		self.logfile = open(logfile, 'a')

	def logga(self, string):
		self.logfile.write(string + '\n')

	def close(self):
		self.logfile.close()

def download_img(links, title):
	import tarfile
	import shutil
	dirname = os.path.dirname(os.path.abspath(sys.argv[0]))
	dirmanga = os.path.join(dirname,'manga')
	directory = os.path.join(dirmanga,title)
	#retcode = subprocess.call([dirname+'/checkdir.sh', directory])
	#if not os.path.isdir(dirmanga):
	#	os.mkdir(dirmanga)
	try:
		os.makedirs(directory)
	except:
		from datetime import datetime
		now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
		os.rename(directory, directory+now)
		os.makedirs(directory)
	os.chdir(dirmanga)
	for link in links:
		file_manga = link[link.rfind('/')+1:]
		for i in range(1,10):
			try:
				urllib.urlretrieve(str(link), os.path.join(directory, file_manga))	
				stampa('  -> scaricato: %s '% (str(link),))
				break
			except:
				from time import sleep
				stampa_err('  -> ERRORE nello scaricare: %s\nRiprovo'% (str(link),))
				sleep(1)
				continue
			stampa_err('  -> ERRORE nello scaricare: %s\nEsco.'% (str(link),))
			sys.exit(-1)

	try:
		tar = tarfile.open(title+'.cbz', 'w')
		tar.add(title)
		tar.close()
		stampa('  Creato %s\n' %(title+'.cbz',))
		shutil.rmtree(title)
	except:
		os.chdir(dirname)
		sys.exit(-1)
	os.chdir(dirname)
	return 1

def download_chapter(url_chapter):
	x = mangareader(url_chapter)
	#manga = x.fetch_title_manga()
	#name = x.convert_name(manga) # converte il nome del manga in formato utile per mangareader
	title = x.convert_name(x.fetch_title_chapter())
	pages = x.fetch_pages_chapter()
	imgs=[]
	imgs.append(x.fetch_link_img())
	for page in pages[1:]: # evitiamo di riscaricare la prima pagina, visto che gia' l'abbiamo
		z = mangareader(page)
		imgs.append(z.fetch_link_img())
	stampa(' -> Trovate %s pagine e %s immagini' % (len(pages),len(imgs)))
	if len(pages) != len(imgs):
		stampa_err('ERRORE: numero di pagine e immagini differente nel capitolo: %s' %(url_chapter,))
		sys.exit(-1)
	#for img in imgs:
	#	stampa('   -> %s' % img)
	if download_img(imgs, title):
		return 1
	sys.exit(-1)

class mangareader:
	def __init__(self, url):
		''' 
		scarica la pagina e compila le regex
		url - stringa che contiene l'indirizzo
		'''
		try:
			usock = urllib.urlopen(url)
			self.page=usock.read()
			usock.close()
		except:
			print "pagina non scaricata: %s" %(url, ) 
			sys.exit(1)
		# compiled regex
		self.rtitlemanga = re.compile('(?<=<title>).*?(?= Manga)')
		self.rtitlechapter = re.compile('(?<=<title>).*?(?= - Read)')
		self.rimg = re.compile('(?<=src=")http://.*jpg(?=")')
		self.roption = re.compile('(?<=option value=").*?(?=")')

	def fetch_tag(self, regex):
		'''
		semplice ricerca per regex
		ritorna 0 oppure lista
		'''
		rows = regex.findall(self.page)
		#if len(rows) == 0:
			#return 0
		return rows 


	def convert_name(self, manga):
		return manga.replace("'","").replace(' - ',' ').replace(' ','-').replace('!','').replace(':','').lower()

	def fetch_title_manga(self):
		'''
		Ritorna il titolo del Manga

		return string
		'''
		return self.fetch_tag(self.rtitlemanga)[0]

	def fetch_title_chapter(self):
		'''
		Ritorna il titolo del capitolo
		solitamente e' nella forma 
		NomeManga NumeroCapitolo

		return string
		'''
		return self.fetch_tag(self.rtitlechapter)[0]
	
	def fetch_pages_chapter(self):
		'''
		ritorna i link delle pagine collegate al capitolo

		return list
		'''
		links=[]
		for row in self.fetch_tag(self.roption):
			links.append(self.build_name(row))
		return links

	def fetch_link_img(self):
		return self.fetch_tag(self.rimg)[0]

	def fetch_chapters_manga(self, nomemanga):
		'''
		ritorna i link dei capitoli collegate ad un manga

		return 0, list
		'''
		regex1 = re.compile('(?<=href=")/' + nomemanga + '.*?(?=")')
		regex2 = re.compile('(?<=href=")/\d*-\d*-\d*/' + nomemanga + '/chapter-\d*.html' + '(?=")')
		links=[]
		rows1 = self.fetch_tag(regex1)
		rows2 = self.fetch_tag(regex2)
		if len(rows1) != 0 :
			for row in rows1:
				if self.build_name(row) not in links:
					links.append(self.build_name(row))
		if len(rows2) != 0 :
			for row in rows2:
				if self.build_name(row) not in links:
					links.append(self.build_name(row))
		if len(links) == 0:
			return 0
		return links



	def build_name (self, link):
		'''
		ricostruisce il link assoluto a partire da un link relativo alla pagina mangareader.net

		link - string
		return string
		'''

		return 'http://www.mangareader.net%s' % (str(link),)

