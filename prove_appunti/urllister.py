from sgmllib import SGMLParser
import string
from string import lower

class URLLister(SGMLParser):
	def reset(self):
		SGMLParser.reset(self)
		self.urls = []
		self.imgs = []
		self.pieces = []

	def start_a(self, attrs):
		href = [v for k, v in attrs if k=='href']
		if href:
			self.urls.extend(href)

	def start_img(self, attrs): 
		#tag = 'provola'
		print attrs
		#strattrs = "".join([' %s="%s"' % (key, value) for key, value in attrs])
		img = [v for k, v in attrs if k=='src']
		if img:
			self.imgs.append(img)

	def unknown_starttag(self, tag, attrs):
		strattrs = "".join([' %s="%s"' % (key, value) for key, value in attrs])
		self.pieces.append("<%(tag)s%(strattrs)s>" % locals())

	def unknown_endtag(self, tag):
		self.pieces.append("</%(tag)s>" % locals())

	def handle_data(self, text):
		self.pieces.append(text)

	def do_meta(self, attributes):
		name = content = ""
		for key, value in attributes:
			if key == "name":
				name = value
			elif key == "content":
				content = value
		if string.lower(name) == "description":
			self.description = content


if __name__ == "__main__":
	import urllib
	#url = raw_input('url: ')
	url = 'http://www.mangareader.net/485-29312-1/claymore/chapter-1.html'
	usock = urllib.urlopen(url)
	parser = URLLister()
	parser.feed(usock.read())
	parser.close()
	usock.close()
	#for url in parser.urls: print url
	for img in parser.imgs: print img
	print '\n\n'
 	for pezzo in parser.pieces:
		print pezzo + '\n'
	print '\n\n'
	print parser.title
