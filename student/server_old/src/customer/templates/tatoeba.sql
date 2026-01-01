CREATE TABLE  IF NOT EXISTS tatoeba.sentences (
        id numeric(10,0) NOT NULL,
        lang char(3) NOT NULL,
        text VARCHAR(400),
        recording VARCHAR(255),
        words VARCHAR(100)[],
        options VARCHAR(400)[],
        PRIMARY KEY (lang, id)
    );

CREATE TABLE  IF NOT EXISTS tatoeba.links (
    id numeric(10,0) NOT NULL,
    translation_id numeric(10,0) NOT NULL,
    PRIMARY KEY (id, translation_id)
);


CREATE TABLE  IF NOT EXISTS tatoeba.info (
    lang3 char(3) NOT NULL,
    lang2 char(2),
    name VARCHAR(100),
    count int4,
    PRIMARY KEY (lang3)
);



CREATE TABLE tatoeba.prepared_sentences (
	id int4 NOT NULL,
	lang char(3) NOT NULL,
	sentence varchar(250) NOT NULL,
	all_words _varchar NULL,
	c_count int4 NULL,
	first varchar(50) NULL,
	first_c varchar(100) NULL,
	last_c varchar(100) NULL,
	pos VARCHAR(20)[],
	propn VARCHAR(30)[],
	root varchar(100) NULL,
	stop_words VARCHAR(25)[] NULL,
	w_count smallint NULL,
	words VARCHAR(30)[] NULL,
	o_count smallint NULL,
	"options" int4[] NULL,
	structure3 varchar(100) NULL,
	structure4 varchar(100) NULL,
	structure_root varchar(100) NULL,
	CONSTRAINT prepared_sentences_pkey PRIMARY KEY (lang, id)
);



CREATE TABLE  IF NOT EXISTS tatoeba.parts (
	lang VARCHAR(12) NOT NULL,
	part_id int4 NOT NULL,
	text VARCHAR(400),
	recording VARCHAR(255),
	words VARCHAR(100)[],
	root VARCHAR(50) NULL,
	options VARCHAR(400)[],
	w_count smallint null default 0,
	PRIMARY KEY (lang, part_id)
);


CREATE TABLE  IF NOT EXISTS tatoeba.links (
    id int4 NOT NULL,
    trans_id int4 NOT NULL,
    PRIMARY KEY (id, trans_id)
);


CREATE TABLE  IF NOT EXISTS tatoeba.links2 (
    id int4 NOT NULL,
	lang char(3) NOT NULL
    trans_id int4 NOT NULL,
    PRIMARY KEY (id, trans_id)
);

CREATE TABLE  IF NOT EXISTS tatoeba.links3 (
    id int4 NOT NULL,
	lang char(3) NOT NULL
    trans_id int4 NOT NULL,
	trans_lang char(3) NOT NULL,
    PRIMARY KEY (lang, trans_lang, id, trans_id)
);

SELECT 
    s1.id,
    s1.lang,
    s2.lang as trans_lang,
    s2.id as trans_id
FROM tatoeba.parts s1
JOIN tatoeba.links l ON s1.id = l.id
JOIN tatoeba.parts s2 ON l.translation_id = s2.id
LIMIT 10;


insert into tatoeba.links2 (id, id_trans)
from select id, id_translation
from tatoeba.links


ALTER TABLE tatoeba.links3
RENAME COLUMN id TO to_id;



CREATE TABLE  IF NOT EXISTS tatoeba.links4 (
	lang char(3) NOT NULL
	to_lang char(3) NOT NULL
    id int4 NOT NULL,
    to_id int4 NOT NULL,
    PRIMARY KEY (lang, to_lang, id, to_id)
);


CREATE TABLE  IF NOT EXISTS tatoeba.words2 (
	lang char(3) NOT null,
	word varchar(80) NOT null,
    ids int4[] ,
    ids_count int4 default 0,
    PRIMARY KEY (lang, word)
);
CREATE TABLE  IF NOT EXISTS tatoeba.steps (
	lang char(3) NOT null,
	step smallint NOT null ,
	word varchar(80) NOT null,
    ids int4[] ,
    ids_count smallint default 0,
    PRIMARY KEY (lang, step)
);


CREATE INDEX idx_array_words_gin ON tatoeba.parts USING GIN (words);


CREATE INDEX parts_lang_w_count ON tatoeba.parts (lang, w_count, words);



select l.*, s.*, s2.*
from tatoeba.links4 l 
join tatoeba.parts s
on s.part_id = l.id
and s.lang = 'ara'
join tatoeba.parts s2
on l.to_id = s2.part_id
and s2.lang = 'eng'
where l.lang = 'ara'
and l.to_lang = 'eng'
and l.id in (608065, 332182 ,332187,332222,332222)



-- final elements 

CREATE TABLE  IF NOT EXISTS tatoeba.steps (
	lang char(3) NOT null,
	step int4 NOT null ,
	word varchar(80) NOT null,
    ids int4[] ,
    ids_count int4 default 0,
    PRIMARY KEY (lang, step)
);
-- to search step by words 
CREATE INDEX idx_words_lang_words ON tatoeba.words2(lang,word ) ;



CREATE TABLE  IF NOT EXISTS tatoeba.lang_info (
	lang char(3) NOT null,
	to_lang char(3) NOT null,
	link_count int4 default 0,
	words VARCHAR(80)[], 
	steps int4[], 
    PRIMARY KEY (lang, to_lang)
);


CREATE TABLE  IF NOT EXISTS tatoeba.steps4 (
	lang char(3) NOT null,
	to_lang char(3) NOT null,
	step int4 NOT null ,
	word varchar(80) NOT null,
    ids int4[] ,
    ids_count int4 default 0,
    PRIMARY KEY (lang, to_lang, step)
);


CREATE TABLE  IF NOT EXISTS tatoeba.lang_info1 (
	lang char(3) NOT null,
	to_lang char(3) NOT null,
	link_count int4 default 0,
	words int4, 
	min_step int4,
	max_step int4, 
    PRIMARY KEY (lang, to_lang)
);




DROP TABLE IF EXISTS tatoeba_users.users;
CREATE TABLE tatoeba_users.users (
	customer_id varchar(100) DEFAULT 'tatoeba'::character varying NOT NULL,
	email varchar(200) NOT NULL,
	user_id varchar(100) NOT NULL,
	user_n_id counter NOT NULL,
	lang char(3)  NULL,
	to_lang char(3)  NULL,
	show_translit boolean DEFAULT false,
	show_text boolean DEFAULT false,
	reverse_mode boolean DEFAULT false,
	last_mode varchar(100)  NULL,
	last_login timestamp DEFAULT now() NULL,
	first_login timestamp DEFAULT now() NULL,
	CONSTRAINT users_pkey PRIMARY KEY (customer_id, email, user_id)
);

DROP TABLE IF EXISTS tatoeba_users.user_words;
CREATE TABLE  IF NOT EXISTS tatoeba_users.user_words (
	user_n_id int4 NOT NULL,
	lang char(3) NOT NULL,
	word varchar(100) NOT NULL,
	mark float8 DEFAULT 0.0 NULL,
	times int4 DEFAULT 0 NULL,
	first_time timestamp DEFAULT now() NULL,
	last_time timestamp DEFAULT now() NULL,
	CONSTRAINT user_words_pkey PRIMARY KEY (user_n_id, lang, word)
);

CREATE TABLE tatoeba_users.user_parts (
	user_n_id int4 NOT NULL,
	lang char(3) NOT NULL,
	part_id varchar(100) NOT NULL,
	mark float8 DEFAULT 0.0 NULL,
	times int4 DEFAULT 0 NULL,
	first_time timestamp DEFAULT now() NULL,
	last_time timestamp DEFAULT now() NULL,
	CONSTRAINT user_parts_pkey PRIMARY KEY (user_n_id, lang, part_id)
);



CREATE TABLE tatoeba_users.user_vocab (
	user_n_id varchar(100) NOT NULL,
	user_id varchar(100) NOT NULL,
	lang char(3) NOT NULL,
	to_lang char(3) NOT NULL,
	last_mode varchar(100) DEFAULT ''::character ,
	mark float8 NULL,
	times int4 NULL,
	first_time timestamp DEFAULT now() NULL,
	last_time timestamp NULL,
	last_step int4 default 1 NULL,
	last_mode varchar(100) DEFAULT ''::character  NULL,
	auto_play bool DEFAULT true NULL,
	show_text bool DEFAULT false NULL,
	reverse_mode bool DEFAULT false NULL,
	show_translit bool DEFAULT false NULL,
	configs jsonb NULL,
	CONSTRAINT user_vocab_pkey PRIMARY KEY (lang, user_id)
);