drop table if exists course.course;

Create table course.course (
    id SERIAL PRIMARY KEY,
    lang varchar(12) not null,
    to_lang varchar(12) not null,
    user_id varchar(100) ,
    title varchar(255) not null,
    description text,
    words varchar(100)[],
    verbs varchar(100)[] ,
    nouns varchar(100)[] ,
    adjectives varchar(100)[] ,
    adverbs varchar(100)[] ,
    auxiliary_verbs varchar(100)[] ,
    vocabulary boolean default false,
    reading boolean default false,
    writing boolean default false,
    grammar boolean default false,
    listening boolean default false,
    speaking boolean default false,
    cultural boolean default false,
    alphabet boolean default false,
    starting_level int2 default 0,
    ending_level int2 default 0,
    created_at timestamp default now(),
    updated_at timestamp default now()
);

