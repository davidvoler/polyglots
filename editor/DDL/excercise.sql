
create table course.exercise (
    id SERIAL PRIMARY KEY,
    course_id int8 not null,
    module_id int8 not null,
    lesson_id int8 not null,
    lang varchar(12) not null,
    to_lang varchar(12) not null,
    user_id varchar(100),
    exercise_type varchar(100) default 'sentence',
    sentence_id int8,
    sentence varchar(300) default '',
    options  varchar(300)[] ,
    to_sentence_id  int8,
    to_sentence  varchar(300) default '',
    to_options  varchar(300)[],
    explanation text,
    extra_data jsonb DEFAULT '{}'::jsonb NULL,
    annotated_sentence jsonb DEFAULT '{}'::jsonb NULL,
    audio_link  varchar(300) default '',
    audio_link_options  varchar(300)[],
    created_at timestamp default now(),
    updated_at timestamp default now()
);