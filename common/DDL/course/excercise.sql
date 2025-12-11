
create table course.exercise (
    id SERIAL PRIMARY KEY,
    lesson_id int8 not null,
    exercise_type varchar(100) default 'sentence',
    sentence_id int8,
    explanation text,
    extra_data jsonb DEFAULT '{}'::jsonb NOT NULL
);


