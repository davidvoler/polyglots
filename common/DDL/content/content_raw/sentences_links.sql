Create table content_raw.sentences_links (
    lang varchar(12) not null,
    id int8 not null,  
    to_lang varchar(12) not null,
    to_id int8 not null,
    translation_source varchar(100),
    primary key (lang, id, to_lang, to_id)
);