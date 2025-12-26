CREATE TABLE content_raw.words_pos1 (
	lang varchar(12) NOT NULL,
	word varchar(100) NOT NULL,
	pos varchar(100) NOT NULL default ,
	root_count int4 DEFAULT 0 NULL,
	wcount int4 DEFAULT 0 NULL,
	sentences_count int4 DEFAULT 0 NULL,
    lemma varchar(100) NOT NULL,
	rank int4 DEFAULT 0 NULL,
	CONSTRAINT words_pos_pkey PRIMARY KEY (lang, word, pos, wcount)
);