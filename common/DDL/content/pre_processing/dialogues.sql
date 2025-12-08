Create table content_raw.dialogues (
    lang varchar(12) not null,
    id int8 not null, -- cityhash of the text - maybe of the first 500 characters
    text text not null,
    source varchar(100) not null,
    words varchar(100)[] not null,
    primary key (lang, id)
);