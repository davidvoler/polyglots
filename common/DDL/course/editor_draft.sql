-- Editor wizard draft: save/resume course creation at last position
drop table if exists course.editor_draft;

create table course.editor_draft (
    id serial primary key,
    created_at timestamptz default now(),
    updated_at timestamptz default now(),
    title varchar(255) not null default '',
    description text default '',
    lang varchar(12) not null,
    to_lang varchar(12) not null,
    selected_question_type_ids text[] default '{}',
    words_with_weight jsonb default '[]',  -- [{"word": "...", "weight": 0}, ...] order preserved
    step int not null default 0,
    automate_lesson boolean default false,
    lessons_per_module int default 10,
    sentences_per_word jsonb default '{}'   -- future: word -> list of sentence ids
);
