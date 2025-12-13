ALTER TABLE content_raw.sentence_elements_preview ADD COLUMN root_lemma varchar(100) NULL;
ALTER TABLE content_raw.sentence_elements_preview ADD COLUMN root varchar(100) NULL;
ALTER TABLE content_raw.sentence_elements_preview ADD COLUMN noun1_lemma varchar(100) NULL;
ALTER TABLE content_raw.sentence_elements_preview ADD COLUMN  verb1_lemma varchar(100) NULL;
ALTER TABLE content_raw.sentence_elements_preview ADD COLUMN  verb1_aux varchar(100) NULL;
ALTER TABLE content_raw.sentence_elements_preview ADD COLUMN   words varchar(100)[] NULL;
ALTER TABLE content_raw.sentence_elements_preview ADD COLUMN   word1 varchar(100) NULL;
ALTER TABLE content_raw.sentence_elements_preview ADD COLUMN   word2 varchar(100) NULL;
ALTER TABLE content_raw.sentence_elements_preview ADD COLUMN   word3 varchar(100) NULL;
ALTER TABLE content_raw.sentence_elements_preview ADD COLUMN   word4 varchar(100) NULL;




ALTER TABLE content_raw.sentence_elements ADD COLUMN root_lemma varchar(100) NULL;
ALTER TABLE content_raw.sentence_elements ADD COLUMN root varchar(100) NULL;
ALTER TABLE content_raw.sentence_elements ADD COLUMN noun1_lemma varchar(100) NULL;
ALTER TABLE content_raw.sentence_elements ADD COLUMN  verb1_lemma varchar(100) NULL;
ALTER TABLE content_raw.sentence_elements ADD COLUMN  verb1_aux varchar(100) NULL;
ALTER TABLE content_raw.sentence_elements ADD COLUMN   words varchar(100)[] NULL;
ALTER TABLE content_raw.sentence_elements ADD COLUMN   word1 varchar(100) NULL;
ALTER TABLE content_raw.sentence_elements ADD COLUMN   word2 varchar(100) NULL;
ALTER TABLE content_raw.sentence_elements ADD COLUMN   word3 varchar(100) NULL;
ALTER TABLE content_raw.sentence_elements ADD COLUMN   word4 varchar(100) NULL;