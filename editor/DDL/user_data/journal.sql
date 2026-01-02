-- user_data.journal definition

-- Drop table

-- DROP TABLE user_data.journal;

CREATE TABLE user_data.journal (
	user_id varchar(100) NOT NULL,
    created_at timestamp DEFAULT now() NULL,
	exercise_id serial4 NOT NULL,
	course_id int8 NOT NULL,
	module_id int8 NOT NULL,
	lesson_id int8 NOT NULL,
	lang varchar(12) NOT NULL,
	to_lang varchar(12) NOT NULL,
	exercise_type varchar(100) DEFAULT 'sentence'::character varying NULL,
    root varchar(100) NULL,
    verb varchar(100) NULL,
    verb_lemma varchar(100) NULL,
    noun varchar(100) NULL,
    adjective varchar(100) NULL,
    auxiliary varchar(100) NULL,
	answer_delay_ms int DEFAULT 0 NULL,
	play_times int DEFAULT 0 NULL,
	attempts int DEFAULT 0 NULL,
	score float DEFAULT 0.0 NULL,
	CONSTRAINT journal_pkey PRIMARY KEY (user_id, created_at)
);



