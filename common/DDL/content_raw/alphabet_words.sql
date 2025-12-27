CREATE TABLE content_raw.alphabet_words (
	lang varchar(12) NOT NULL,
	word varchar(100) NOT NULL,
	pos varchar(100) NOT NULL default '' ,
	root_count int4 DEFAULT 0 NULL,
	wcount int4 DEFAULT 0 NULL,
	sentences_count int4 DEFAULT 0 NULL,
    lemma varchar(100) NOT NULL,
	rank int4 DEFAULT 0 NULL,
	kanji_count int default 0,
	hiragana_count int default 0,
	katakana_count int default 0,
	kanji_letters varchar(10) NULL,
	hiragana_letters varchar(10) NULL,
	katakana_letters varchar(10) NULL,
	CONSTRAINT alphabet_words_pkey PRIMARY KEY (lang, word, pos, wcount)
);