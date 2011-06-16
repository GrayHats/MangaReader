import re
import urllib
def get_tag(starttag, endtag, regex, html):
	finder=re.compile('(?<='+starttag+')'+regex+'(?='+endtag+')')
	return finder.findall(html)
url = 'http://www.mangareader.net/485-29312-1/claymore/chapter-1.html'
usock = urllib.urlopen(url)
page1 = usock.read()
usock.close()

url2 = 'http://www.mangareader.net/claymore/113'
usock = urllib.urlopen(url2)
page2 = usock.read()
usock.close()

url3 ='http://www.mangareader.net/485/claymore.html'
usock = urllib.urlopen(url3)
page3 = usock.read()
usock.close()

'''
example title
>>> print prova.get_tag('<title>','</title>','.*?',prova.page)
['Claymore 1 - Read Claymore 1 Online - Page 1']

example img

>>> print prova.get_tag('src="','"','http://.*jpg',prova.page)
['http://i1.mangareader.net/claymore/1/claymore-697017.jpg']


example option
>>> print prova.get_tag('option value="','"','.*?',prova.page)
...funge per entrambe le due pagine

'''
