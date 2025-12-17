drop table if exists template.course_module;

Create table template.course_module (
    id SERIAL PRIMARY KEY,
    lang varchar(12) not null default '',
    name varchar(255) not null,
    description text,
    words_count int2 default 20,
    level int2 default 1,
    lesson_tags varchar(255)[] default '[]'::varchar(255)[], -- like new_words, grammar, vocabulary, etc.
    sentences_length int2 default 5,
    verb_count int2 default 2,
    noun_count int2 default 2,
    adjective_count int2 default 1,
    adverb_count int2 default 0,
    preposition_count int2 default 0,
    conjunction_count int2 default 0,
    pronoun_count int2 default 0,
    interjection_count int2 default 0,
    auxiliary_verb_count int2 default 0,
    created_at timestamp default now(),
    updated_at timestamp default now()
);