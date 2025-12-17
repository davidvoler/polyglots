drop table if exists template.lesson;

Create table template.lesson (
    id SERIAL PRIMARY KEY,
    lang varchar(12) not null default '',
    name varchar(255) not null,
    description text,
    words_count int2 default 20,
    level int2 default 1,

    vocabulary boolean default false,
    reading boolean default false,
    writing boolean default false,
    grammar boolean default false,
    listening boolean default false,
    speaking boolean default false,
    cultural boolean default false,
    alphabet boolean default false,
    greetings boolean default false,
    custom_content varchar(255)[] default '[]'::varchar(255)[], -- like kanji, hiragana, katakana, etc.
    max_word_count int2 default 5,
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