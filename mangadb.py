'''
funzioni e classi
'''
from storm.locals import Date, Unicode, DateTime, Int, \
        create_database, Store, Storm, Reference

from mangareader import dirname
from os import path

database = create_database("sqlite:" + path.join(dirname, "database"))
store = Store(database)



class Chapter(Storm):
    '''
    Oggetto gestito da Storm
    '''
    __storm_table__ = "chapters"
    id = Int(primary=True)
    name = Unicode()
    number = Int()
    status = Int()
    id_manga = Int()
    link = Unicode()
    data = DateTime()
    manga = Reference(id_manga, "Manga.id")

    def __repr__(self):
        return "<Chapter('%s', '%s', '%s', '%s', '%s', '%s', '%s')>" \
                % (self.id, self.name, self.number, \
                self.link, self.status, self.data, self.id_manga)

class Manga(Storm):
    '''
    Oggetto gestito da Storm
    '''
    __storm_table__ = "mangas"
    id = Int(primary=True)
    name = Unicode()
    link = Unicode()
    status = Int()
    data = DateTime()

    def __repr__(self):
        return "<Manga('%s', '%s', '%s', '%s', '%s')>" \
                % (self.id, self.name, self.link, \
                self.status, self.data)


class Mail(Storm):
    '''
    Oggetto gestito da Storm
    '''
    __storm_table__ = "mails"
    id = Int(primary=True)
    from_addr = Unicode()
    to_addr = Unicode()
    subject = Unicode()
    smtp = Unicode()

    def __repr__(self):
        return "<mail('%s', '%s', '%s', '%s', '%s')>" \
                % (self.id, self.from_addr, self.to_addr, \
                self.subject, self.smtp)

