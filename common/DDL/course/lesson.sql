Create table course.lesson (
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
    auxiliary_verbs varchar(100)[]
);