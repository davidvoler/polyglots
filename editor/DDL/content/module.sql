-- course."module" definition

-- Drop table

-- DROP TABLE course."module";

CREATE TABLE content."module" (
	module_id serial4 NOT NULL,
	course_id int8 NOT NULL,
	lang varchar(12) NOT NULL,
	to_lang varchar(12) NOT NULL,
	user_id varchar(100) NULL,
	title varchar(255) NOT NULL,
	description text NULL,
    lesson_count int2 DEFAULT 0 NULL,
    exercise_count int2 DEFAULT 0 NULL,
    weight int2 DEFAULT 0 NULL,
	words _varchar NULL,
	verbs _varchar NULL,
	nouns _varchar NULL,
	adjectives _varchar NULL,
	adverbs _varchar NULL,
	auxiliary_verbs _varchar NULL,
	vocabulary bool DEFAULT false NULL,
	reading bool DEFAULT false NULL,
	writing bool DEFAULT false NULL,
	grammar bool DEFAULT false NULL,
	listening bool DEFAULT false NULL,
	speaking bool DEFAULT false NULL,
	cultural bool DEFAULT false NULL,
	alphabet bool DEFAULT false NULL,
	max_word_count int2 DEFAULT 4 NULL,
	created_at timestamp DEFAULT now() NULL,
	updated_at timestamp DEFAULT now() NULL,
	CONSTRAINT module_pkey PRIMARY KEY (module_id)
);