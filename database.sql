create table mangas (id INTEGER PRIMARY KEY ASC, name TEXT, link TEXT, status INTEGER, data TEXT );

create table chapters (id INTEGER PRIMARY KEY ASC, name TEXT, number INTEGER, link TEXT, status INTEGER, data TEXT, id_manga INTEGER);

