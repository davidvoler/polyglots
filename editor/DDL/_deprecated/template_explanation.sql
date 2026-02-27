drop table if exists template.lesson;


Create table template.explanation (
    id SERIAL PRIMARY KEY,
    lang varchar(12) not null default '',
    name varchar(255) not null,
    description text,
    tags varchar(255)[] default '[]'::varchar(255)[],
    examples varchar(255)[] default '[]'::varchar(255)[],
    );