'''
funzioni e classi
'''
import urllib
import requests
import re
import sys
import os
from time import sleep

dirname = os.path.dirname(os.path.abspath(sys.argv[0]))


def stampa(stringa):
    '''
    semplice funzione che stampa
    stringa --> string
    '''
    sys.stdout.write(stringa + '\n')


def stampa_err(string):
    '''
    semplice funzione che stampa errori
    stringa --> string
    '''
    sys.stderr.write(string + '\n')
    from datetime import datetime
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_err = os.path.join(dirname, 'log_error')
    log = open(file_err, 'a')
    log.write('%s: %s%s' % (now, string, '\n'))
    log.close()


class logfile:

    def __init__(self, logfile):
        self.logfile = open(logfile, 'a')

    def logga(self, string):
        self.logfile.write(string + '\n')

    def close(self):
        self.logfile.close()


def fix_title(name):
    regex = re.compile('(.*?)-(\d{1})$')
    if regex.search(name):
        return '%s-00%s' % (regex.search(name).group(1),
                            regex.search(name).group(2))
    regex = re.compile('(.*?)-(\d{2})$')
    if regex.search(name):
        return '%s-0%s' % (regex.search(name).group(1),
                           regex.search(name).group(2))
    return '%s' % name


def createdir(directory):
    """
    crea una directory,
    se esiste gia', rinomina e crea
    manca un controllo degli errori di i/o
    """
    if os.path.exists(directory):
        from datetime import datetime
        now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        os.rename(directory, directory+now)
    os.mkdir(directory)


def build_cbt(links, title):
    import tarfile
    import shutil
    dirname = os.path.dirname(os.path.abspath(sys.argv[0]))
    dirmanga = os.path.join(dirname, 'manga')
    directory = os.path.join(dirmanga, title)
    createdir(directory)
    os.chdir(dirmanga)
    for link in links:
        link = str(link)
        # file_manga = link[link.rfind('/')+1:]
        file_name = os.path.join(directory, link.split('/')[-1])
        for i in range(1, 10):
            try:
                download_file(link, file_name)
                stampa('  -> scaricato: %s ' % (link,))
                sleep(1)
                break
            except:
                stampa_err('  -> ERRORE nello scaricare: %s' % (link))
                stampa_err('  -> impossibile creare %s' % (file_name))
                stampa_err('Riprovo')
                sleep(1)
                continue
            exit('  -> ERRORE nello scaricare: %s\
                    \nEsco.' % (link,))

    try:
        tar = tarfile.open(title+'.cbt', 'w')
        tar.add(title)
        tar.close()
        stampa('  Creato %s\n' % (title+'.cbt',))
        shutil.rmtree(title)
    except:
        os.chdir(dirname)
        sys.exit(-1)
    os.chdir(dirname)
    return 1


def download_file(url, local_filename):
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename


def download_chapter(url_chapter):
    x = mangareader(url_chapter)
    title = x.convert_name(x.fetch_title_chapter())
    pages = x.fetch_pages_chapter()
    imgs = []
    imgs.append(x.fetch_link_img())
    for page in pages[1:]:
        # evitiamo di riscaricare la prima pagina, visto che gia' l'abbiamo
        z = mangareader(page)
        imgs.append(z.fetch_link_img())
    stampa(' -> Trovate %s pagine e %s immagini' % (len(pages), len(imgs)))
    if len(pages) != len(imgs):
        stampa_err('ERRORE: numero di pagine e immagini differente \
                nel capitolo: %s' % (url_chapter,))
        return 0
    # for img in imgs:
    #    stampa('   -> %s' % img)
    if build_cbt(imgs, fix_title(title)):
        return 1
    # sys.exit(-1)


class mangareader:

    def __init__(self, url):
        '''
        scarica la pagina e compila le regex
        url - stringa che contiene l'indirizzo
        '''

        for i in range(1, 10):
            try:
                usock = urllib.urlopen(url)
                self.page = usock.read()
                usock.close()
                break
            except:
                from time import sleep
                stampa_err('  -> ERRORE nello scaricare: %s\
                        \nRiprovo' % (str(url),))
                sleep(1)
                continue
            exit('  -> ERRORE nello scaricare: %s\
                    \nEsco.' % (str(url),))
        # compiled regex
        self.rtitlemanga = re.compile('(?<=<title>).*?(?= Manga)')
        self.rtitlechapter = re.compile('(?<=<title>).*?(?= - Read)')
        self.rimg = re.compile('(?<=src=")http://.*jpg(?=")')
        self.roption = re.compile('(?<=option value=").*?(?=")')
        self.findnumber1 = re.compile(r'(?<=/chapter-)\d+(?=.html$)')
        self.findnumber2 = re.compile(r'(?<=/)\d+$')

    def fetch_tag(self, regex):
        '''
        semplice ricerca per regex
        ritorna 0 oppure lista
        '''
        rows = regex.findall(self.page)
        # if len(rows) == 0:
        #   return 0
        return rows

    def convert_name(self, manga):
        return manga.replace("'", "")\
            .replace(' - ', ' ')\
            .replace(' ', '-')\
            .replace('!', '')\
            .replace('/', '')\
            .replace(':', '')\
            .replace('%', '')\
            .replace(';', '')\
            .replace('&', '')\
            .replace('(', '')\
            .replace(')', '')\
            .lower()

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

    def number(self, stringa):
        match = self.findnumber1.search(stringa)
        if match:
            return match.group(0)
        match = self.findnumber2.search(stringa)
        if match:
            return match.group(0)
        print 'nessun numero capitolo trovato??'
        return 0

    def find_manga(self, name):
        '''
         cerca in una pagina per vedere se trova il nome del manga cercato
        '''
        regex1 = r'(?<=<a href=")/%s(?=")' % name
        regex2 = r'(?<=<a href=")/\d+/%s.html(?=")' % name
        match = re.search(regex1, self.page)
        if match:
            return self.build_name(match.group(0))
        match = re.search(regex2, self.page)
        if match:
            return self.build_name(match.group(0))
        print '--> %s non trovato??' % name
        return 0

    def fetch_pages_chapter(self):
        '''
        ritorna i link delle pagine collegate al capitolo

        return list
        '''
        links = []
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
        regex1 = re.compile('(?<=href=")/' + nomemanga + '/.*?(?=")')
        regex2 = re.compile(
            '(?<=href=")/\d*-\d*-\d*/' + nomemanga +
            '/chapter-\d*.html' + '(?=")')
        links = []
        rows1 = self.fetch_tag(regex1)
        rows2 = self.fetch_tag(regex2)
        if len(rows1) != 0:
            for row in rows1:
                chapter = self.build_name(row)
                number = self.number(chapter)
                if (chapter, number) not in links:
                    links.append((chapter, number))
        if len(rows2) != 0:
            for row in rows2:
                chapter = self.build_name(row)
                number = self.number(chapter)
                if (chapter, number) not in links:
                    links.append((chapter, self.number(chapter)))
        if len(links) == 0:
            return 0
        return links

    def build_name(self, link):
        '''
        ricostruisce il link assoluto a partire da un link relativo
        alla pagina mangareader.net

        link - string
        return string
        '''

        return 'http://www.mangareader.net%s' % (str(link),)
