drop table if exists course.module;

Create table course.module (
    id SERIAL PRIMARY KEY,
    course_id int8 not null,
    lang varchar(12) not null,
    to_lang varchar(12) not null,
    user_id varchar(100) ,
    title varchar(255) not null,
    description text,
    words varchar(100)[] ,
    verbs varchar(100)[] ,
    nouns varchar(100)[] ,
    adjectives varchar(100)[] ,
    adverbs varchar(100)[] ,
    auxiliary_verbs varchar(100)[],
    vocabulary boolean default false,
    reading boolean default false,
    writing boolean default false,
    grammar boolean default false,
    listening boolean default false,
    speaking boolean default false,
    cultural boolean default false,
    alphabet boolean default false,
    max_word_count int2 default 4,
    created_at timestamp  default now(),
    updated_at timestamp default now()
);