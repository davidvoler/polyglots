Create table content_raw.dialogues_links (
    lang varchar(12) not null,
    id int8 not null, -- cityhash of the text in sentence - easier to work with than string 
    to_lang varchar(12) not null,
    to_id int8 not null, -- cityhash of the text in sentence - easier to work with than string 
    translation_source varchar(100) not null,
    primary key (lang, id, to_lang, to_id)
);



CREATE TABLE content_raw.translation_links1 (
	lang varchar(12) NOT NULL,
	id int8 NOT NULL,
	to_lang varchar(12) NOT NULL,
	to_id int8 NOT NULL,
	corpus varchar(12) NULL,
	machine bool DEFAULT false NULL,
	direct bool DEFAULT false NULL,
	CONSTRAINT translation_links_pkey PRIMARY KEY (lang, id, to_lang, to_id)
);



insert into content_raw.translation_links1(
    lang, id, to_lang, to_id, corpus, machine, direct

)
select lang, CAST(id AS int8), to_lang, CAST(to_id AS int8), corpus, machine, direct
from content_raw.translation_links