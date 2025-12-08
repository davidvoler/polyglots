create table content.sentences (
    lang char(3) not null,
    to_lang char(3) not null,
    id int8 not null,
    text varchar(255) not null,
	to_text varchar(255) not null,
    translit varchar(255), 
    recording varchar(255) not null,
    words varchar(100)[] not null,
	options varchar(255)[] NULL,
	to_options varchar(255)[] NULL,
    elements jsonb DEFAULT '[]'::jsonb NOT NULL,
	verbs varchar(100)[] NULL,
	auxiliary_verbs varchar(100)[] NULL,
	nouns varchar(100)[] NULL,
	adjectives varchar(100)[] NULL,
    primary key (lang, to_lang, id)
);


create table content.explanation (
    lang char(3) not null,
    to_lang char(3) not null,
    id int8 not null,
    text varchar(255) not null,
    recording varchar(255) not null,
    elements jsonb DEFAULT '[]'::jsonb NOT NULL,
	tags varchar(100)[] NULL,
    primary key (lang, to_lang, id)
);


