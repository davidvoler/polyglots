Create table content_raw.dialogues_links (
    lang varchar(12) not null,
    id int8 not null, -- cityhash of the text in sentence - easier to work with than string 
    to_lang varchar(12) not null,
    to_id int8 not null, -- cityhash of the text in sentence - easier to work with than string 
    translation_source varchar(100) not null,
    primary key (lang, id, to_lang, to_id)
);