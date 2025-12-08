Create table content_raw.batch_status (
    action varchar(12),
    is_preview boolean default false,
    batch_id varchar(20),
    limit int,
    primary key (action,batch_id)
);


