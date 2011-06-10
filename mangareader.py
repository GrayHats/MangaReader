import urllib2
import urllib
from BeautifulSoup import BeautifulSoup
import re
import sys, os
import tarfile
import shutil
from datetime import datetime

def put(string):
	sys.stdout.write(string + '\n')

def put_err(string):
	sys.stderr.write(string + '\n')


class logfile:
	def __init__(self, logfile):
		self.logfile = open(logfile, 'a')

	def logga(self, string):
		self.logfile.write(string + '\n')

	def close(self):
		self.logfile.close()


def download_img(links, title):
	dirname = os.path.dirname(os.path.abspath(sys.argv[0]))
	dirmanga = os.path.join(dirname,'manga')
	directory = os.path.join(dirmanga,title)
	#retcode = subprocess.call([dirname+'/checkdir.sh', directory])
	#if not os.path.isdir(dirmanga):
	#	os.mkdir(dirmanga)
	try:
		os.makedirs(directory)
	except:
		now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
		os.rename(directory, directory+now)
		os.makedirs(directory)
	os.chdir(dirmanga)
	for link in links:
		file_manga = link[link.rfind('/')+1:]
		urllib.urlretrieve(str(link), os.path.join(directory, file_manga))	
		#print 'scaricato %s '% (str(link),)
	try:
		tar = tarfile.open(title+'.cbz', 'w')
		tar.add(title)
		tar.close()
		shutil.rmtree(title)
	except:
		os.chdir(dirname)
		return 0
	os.chdir(dirname)
	return 1

def download_chapter(url_chapter):
	x = mangareader(url_chapter)
	manga = x.fetch_title()
	name = x.convert_name(manga) # converte il nome del manga in formato utile per mangareader
	title = x.convert_name(str(x.fetch_links('%s \d\d*' % (manga), 'title')[0]))
	#<option value="/fairy-tail/216/5">5</option>
	pages = []
	pages = x.fetch_links('/\d*-\d*-\d*/%s/.*html' %(name), 'option',1)	
	if len(pages) == 0:
		pages = x.fetch_links('/%s/\d\d*/\d\d*' %(name), 'option',1)	
	pages.insert(0,url_chapter)
	links=[]
	for page in pages:
		z = mangareader(str(page))
		for link in z.fetch_links('http://.*%s.*jpg' %(name),'src'):
			links.append(link)
	download_img(links, title)
	return 1

class mangareader:
	def __init__(self, url):
		''' fetch the page and parse with beatifulsoup'''
		try:
			page = urllib2.urlopen(url)
		except:
			print "pagina non scaricata: %s" %(url, ) 
			sys.exit(1)
		self.soup = BeautifulSoup(page)	
		#self.manga = self_title

	def looking_for(self, manga):
		'''example: looking for Fairy Tail release'''
		trovato = self.soup.findAll(text=re.compile('%s \d*' % (manga,)))
		if trovato:
			return trovato
		else:
			return 0

	def convert_name(self, manga):
		return manga.replace("'","").replace(' - ',' ').replace(' ','-').lower()

	def fetch_title(self):
		raw_title = self.soup.title.contents[0]
		p1 = re.search('.*(?= Manga)',raw_title)
		if not p1:
			p2=re.search('.*(?= \d+ - Read)', raw_title)
			return p2.group(0)
		return p1.group(0)
		##p4=re.compile('\d+$')   #appunto per trovare il numero di capitolo

	def fetch_chapter(self):
		raw_title = self.soup.title.contents[0]
		p2=re.search('.*(?= - Read)', raw_title)
		return p2.group(0)
		##p4=re.compile('\d+$')   #appunto per trovare il numero di capitolo

	def fetch_links(self, regexpr, attr='href', convert=0):
		'''Fetch links for a centain manga '''
		## looking for links 
		links = [] # they can be more than 1 :D
		p = re.compile(regexpr)
		if attr == 'option':
			rows=self.soup.findAll(value=re.compile(regexpr))
		elif attr == 'src':
			rows=self.soup.findAll(src=re.compile(regexpr))
		elif attr == 'title':
			rows=self.soup.findAll('title')
		else :
			rows=self.soup.findAll(href=re.compile(regexpr))
		if rows:
			for row in rows:
				if convert == 1:
					links.append(self.build_name(p.findall(str(row))[0]))
					continue
				links.append(p.findall(str(row))[0])
		return links

	def build_name (self, link):
		return 'http://www.mangareader.net%s' % (str(link),)

