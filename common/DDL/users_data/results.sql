create table users_data.results (
    id auto_increment,
    user_id varchar(100) not null,
    lang char(3) not null,
    to_lang char(3) not null,
    course_id int8 not null,
    lesson_id int8 not null,
    question_id int8 not null,
    question_type str(100) not null,
    result jsonb not null,
    primary key (id)
);