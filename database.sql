create table mangas (id INTEGER PRIMARY KEY ASC, name TEXT, link TEXT, status INTEGER );

create table chapters (id INTEGER PRIMARY KEY ASC, name TEXT, number INTEGER, link TEXT, status INTEGER, id_manga INTEGER);

create table pics (id INTEGER PRIMARY KEY ASC, link TEXT, status INTEGER, id_chapter INTEGER);
