Create table content_raw.dialogues (
    lang varchar(12) not null,
    group_by varchar(100),
    group_id int8 default 0,
    ids int8[] default '{}',
    count_ids int8 default 0,
    min_words_count int2 default 0,
    max_words_count int2 default 0,
    reviewed boolean default false,
    review_comments text,
    primary key (lang, group_by, group_id)
);