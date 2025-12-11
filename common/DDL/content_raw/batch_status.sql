CREATE TABLE content_raw.batch_status (
	batch_id bpchar(36) NOT NULL,
	"action" varchar(12) NOT NULL,
	lang varchar(12) NULL,
	to_lang varchar(12) NULL,
	stage varchar(12) NULL,
	operation varchar(12) NULL,
	corpus varchar(12) NULL,
	review bool NULL,
	"limit" int4 NULL,
	"offset" int4 NULL,
	is_preview bool DEFAULT false NULL,
	created_at timestamp DEFAULT now() NOT NULL,
	CONSTRAINT batch_status_pkey PRIMARY KEY (batch_id, action, created_at)
);