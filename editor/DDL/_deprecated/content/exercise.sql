DROP TABLE content.exercise;

CREATE TABLE content.exercise (
	exercise_id serial4 NOT NULL,
	course_id int8 NOT NULL,
	module_id int8 NOT NULL,
	lesson_id int8 NOT NULL,
	lang varchar(12) NOT NULL,
	to_lang varchar(12) NOT NULL,
	weight int2 DEFAULT 0 NULL,
	-- exercise data 
	exercise_type varchar(100) DEFAULT 'sentence'::character varying NULL,
	title varchar(300) NULL,
	instruction varchar(300) NULL,
	sentence varchar(300) DEFAULT ''::character varying NULL,
	correct_options varchar(300)[] NULL,
	wrong_options varchar(300)[] NULL,
	annotated_sentence jsonb DEFAULT '{}'::jsonb NULL,
	extra_data jsonb DEFAULT '{}'::jsonb NULL,
	explanation text NULL,
	audio_link varchar(300) DEFAULT ''::character varying NULL,
    -- extra data 
    root varchar(100) NULL,
    verb varchar(100) NULL,
    verb_lemma varchar(100) NULL,
    noun varchar(100) NULL,
    adjective varchar(100) NULL,
    auxiliary varchar(100) NULL,
	letter varchar(10) NULL,
	ab_type varchar(10) DEFAULT '' NULL,
	word varchar(100) DEFAULT '' NULL,
	-- authoring data 
    sentence_id int8 NULL,
    to_sentence_id int8 NULL,
    user_id varchar(100) NULL,
    created_at timestamp DEFAULT now() NULL,
	updated_at timestamp DEFAULT now() NULL,
	CONSTRAINT exercise_pkey PRIMARY KEY (exercise_id)
);