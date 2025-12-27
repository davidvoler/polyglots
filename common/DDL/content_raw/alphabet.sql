CREATE TABLE content_raw.alphabet (
	lang varchar(12) NOT NULL,
	ab_type char(1) NOT NULL default '',
	letter varchar(5) NOT NULL,
	words_count int4 default 0,
	CONSTRAINT alphabet_pkey PRIMARY KEY (lang, ab_type,letter)
);