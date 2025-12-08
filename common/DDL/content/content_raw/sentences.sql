Create table content_raw.sentences (
    lang varchar(12) not null,
    id int8 not null, -- cityhash of the text in sentence - easier to work with than string 
    text varchar(300) not null,
    source varchar(100),
    primary key (lang, id)
);