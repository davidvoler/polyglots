crate table courses.course (
    id auto_increment,
    lang char(3) not null,
    user_id varchar(100) ,
    to_lang char(3) not null,
    lesson_id int8 not null,
    title varchar(255) not null,
    description text,
    primary key (id)
);


create table courses.lesson (
    id auto_increment,
    course_id int8 not null,
    user_id varchar(100),
    lang char(3) not null,
    to_lang char(3) not null,
    lesson_id int8 not null,
    step_id int8 not null,
    title varchar(255) not null,
    description text,
    primary key (course_id, id)
);