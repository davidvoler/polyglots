ALTER TABLE content_raw.sentence_elements_preview ADD COLUMN root_lemma varchar(100) NULL;
ALTER TABLE content_raw.sentence_elements_preview ADD COLUMN root varchar(100) NULL;
ALTER TABLE content_raw.sentence_elements_preview ADD COLUMN noun1_lemma varchar(100) NULL;
ALTER TABLE content_raw.sentence_elements_preview ADD COLUMN  verb1_lemma varchar(100) NULL;
ALTER TABLE content_raw.sentence_elements_preview ADD COLUMN  verb1_aux varchar(100) NULL;