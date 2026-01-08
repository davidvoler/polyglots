-- user_data.user_info definition

-- Drop table

-- DROP TABLE user_data.user_info;

CREATE TABLE user_data.user_info (
	user_id varchar(100) NOT NULL,
    lang varchar(12) NOT NULL,
	to_lang varchar(12) NOT NULL,
	created_at timestamp DEFAULT now() NULL,
	course_id int8 NOT NULL,
	module_id int8 NOT NULL,
	lesson_id int8 NOT NULL,
	CONSTRAINT user_info_pkey PRIMARY KEY (user_id,lang,to_lang)
);