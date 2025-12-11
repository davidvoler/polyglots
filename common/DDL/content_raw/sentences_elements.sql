DROP TABLE content_raw.sentence_elements;

CREATE TABLE content_raw.sentence_elements (
	lang varchar(12) NOT NULL,
	id int8 NOT NULL,
	"text" varchar(300) NOT NULL,
	elements jsonb DEFAULT '[]'::jsonb NULL,
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
	len_c int2 DEFAULT 0 NULL,
	len_elm int2 NULL,
	lang_extra jsonb DEFAULT '{}'::jsonb NULL,
	CONSTRAINT sentence_elements1_pkey PRIMARY KEY (lang, id)
);