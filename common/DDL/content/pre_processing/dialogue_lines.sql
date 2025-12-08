Create table content_raw.dialogues (
    lang varchar(12) not null,
    dialogue_id int8 notnull,
    line_no int2 default 0,
    text varchar(300) ,
    source varchar(100) not null,
    spacy_analysis jsonb,
    transliteration jsonb,
    element_tags jsonb,
    elements jsonb DEFAULT '[]'::jsonb NOT NULL,
	verbs varchar(100)[] NULL,
	auxiliary_verbs varchar(100)[] NULL,
	nouns varchar(100)[] NULL,
	adjectives varchar(100)[] NULL,
    reviewed boolean  default false,
    review_comments text,
    primary key (lang, id)
);