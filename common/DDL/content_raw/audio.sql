
create table content_raw.audio (
    lang varchar(12) not null,
    id int8 not null, -- cityhash of the text in sentence - easier to work with than string 
    recording varchar(255) not null,
    audio_engine varchar(100) not null default '',
    voice varchar(100) not null default '',
    gender varchar(100),
    age varchar(100),
    primary key (audio_engine,voice, lang, id)
);