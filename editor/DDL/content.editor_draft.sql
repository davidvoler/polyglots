-- "content".editor_draft definition

-- Drop table

-- DROP TABLE "content".editor_draft;

CREATE TABLE "content".editor_draft (
	id serial4 NOT NULL,
	created_at timestamptz DEFAULT now() NULL,
	updated_at timestamptz DEFAULT now() NULL,
	title varchar(255) DEFAULT ''::character varying NOT NULL,
	description text DEFAULT ''::text NULL,
	lang varchar(12) NOT NULL,
	to_lang varchar(12) NOT NULL,
	selected_question_type_ids _text DEFAULT '{}'::text[] NULL,
	words_with_weight jsonb DEFAULT '[]'::jsonb NULL,
	step int4 DEFAULT 0 NOT NULL,
	automate_lesson bool DEFAULT false NULL,
	lessons_per_module int4 DEFAULT 10 NULL,
	sentences_per_word jsonb DEFAULT '{}'::jsonb NULL,
	CONSTRAINT content_editor_draft_pkey PRIMARY KEY (id)
);