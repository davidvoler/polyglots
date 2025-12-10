--DROP TABLE content_raw.sentence_elements;

CREATE TABLE content_raw.sentence_elements1 (
	lang varchar(12) not null,
	id int8 not null,
	text varchar(300) not null,
	elements jsonb DEFAULT '[]'::jsonb ,
	adverb1 text NULL,
	adverb2 text NULL,
	verb1 text NULL,
	verb2 text NULL,
	auxiliary_verb1 text NULL,
	auxiliary_verb2 text NULL,
	noun1 text NULL,
	noun2 text NULL,
	adjective1 text NULL,
	adjective2 text NULL,
	verb_count int2 DEFAULT 0 NULL,
	noun_count int2 DEFAULT 0 NULL,
	adjective_count int2 DEFAULT 0 NULL,
	adverb_count int2 DEFAULT 0 NULL,
    len_c int2 default 0,
    len_elm int2 default 0,
    lang_extra jsonb DEFAULT '{}'::jsonb ,
	CONSTRAINT sentence_elements_pkey PRIMARY KEY (lang, id)
);



DROP TABLE content_raw.sentence_elements;
CREATE TABLE content_raw.sentence_elements (
	lang varchar(12) NOT NULL,
	id varchar(255) NOT NULL,
	text varchar(300) NOT NULL,
	elements jsonb DEFAULT '[]'::jsonb NOT NULL,
	adverb1 text NULL,
	adverb2 text NULL,
	verb1 text NULL,
	verb2 text NULL,
	auxiliary_verb1 text NULL,
	auxiliary_verb2 text NULL,
	noun1 text NULL,
	noun2 text NULL,
	adjective1 text NULL,
	adjective2 text NULL,
	verb_count int2 DEFAULT 0 NULL,
	noun_count int2 DEFAULT 0 NULL,
	adjective_count int2 DEFAULT 0 NULL,
	adverb_count int2 DEFAULT 0 NULL,
	CONSTRAINT japanese_sentence_elements_pkey PRIMARY KEY (lang, part_id)
);



DROP TABLE content_raw.ja_sentence_elements;

CREATE TABLE content_raw.ja_sentence_elements (
	lang varchar(12) NOT NULL,
	id varchar(255) NOT NULL,
	text varchar(300) NOT NULL,
	kanji_count int4 DEFAULT 0 NOT NULL,
	hiragana_count int4 DEFAULT 0 NOT NULL,
	katakana_count int4 DEFAULT 0 NOT NULL,
	other_count int4 DEFAULT 0 NOT NULL,
	unique_kanji_letters varchar(255) NULL,
	unique_hiragana_letters varchar(255) NULL,
	unique_katakana_letters varchar(255) NULL,
	CONSTRAINT japanese_sentence_elements_pkey PRIMARY KEY (lang, part_id)
);



alter table  content_raw.sentence_elements1 remove columns 
	
	kanji_count ,
	hiragana_count  ,
	katakana_count  ,
	other_count ,
	unique_ab1_letters ,
	unique_ab2_letters ,
	unique_ab3_letters ;



CREATE TABLE content_raw.translation_links (
	lang varchar(12) NOT NULL,
	id varchar(255) NOT NULL,
    to_lang varchar(12) NOT NULL,
	to_id varchar(255) NOT NULL,
    machine boolean default false,
    direct boolean default false,
	CONSTRAINT translation_links_pkey PRIMARY KEY (lang, part_id)
);
