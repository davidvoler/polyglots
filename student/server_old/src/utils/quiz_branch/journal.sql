-- jounral table that has all the data

create table tatoeba_users.journal1 (
    user_id varchar(100) not null,
    lang char(3) not null,
    ts timestamp not null,
    step varchar(100) not null,
    mark float default 0.0,
    part_id int4,
    word1 varchar(150),
    word2 varchar(150),
    word3 varchar(150),
    branch_key varchar(255),
    branch_word varchar(150),
    wcount int default 0,
    answer_delay_ms= int default 0,
    play_times int default 0,
    attempts int default 0,
    primary key (user_id, lang, ts)
);