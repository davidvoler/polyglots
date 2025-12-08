Create table content_raw.audio (
    corpus varchar(12) not null,
    description text,
    url varchar(255) ,
    ai_generated boolean default false,
    primary key (corpus)
   
);