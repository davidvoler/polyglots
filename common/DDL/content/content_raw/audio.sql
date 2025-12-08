Create table content_raw.audio (
    lang varchar(12) not null,
    id int8 not null, -- cityhash of the text in sentence - easier to work with than string 
    url varchar(100) not null,
    voice varchar(100) not null,
    source varchar(100),
    primary key (lang, id, url)
);