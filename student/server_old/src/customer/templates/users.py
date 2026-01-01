from string import Template

# Template for user_parts table
user_content_table = Template("""
DROP TABLE IF EXISTS ${customer_id}_users.user_content;
CREATE TABLE  IF NOT EXISTS ${customer_id}_users.user_content (
    lang VARCHAR(12) NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    part_id VARCHAR(300) default '',
    step varchar(100) default '',
    dialogue_id VARCHAR(100) default '',
    dialogue_line VARCHAR(105) default '',
    tag VARCHAR(100) default '',
    level INT,
    mark FLOAT,
    times INT,
    first_time TIMESTAMP DEFAULT NOW(),
    last_time TIMESTAMP,
    PRIMARY KEY (lang, user_id, part_id, dialogue_id, dialogue_line)
);
""")

# Template for user_journal table
user_journal_table = Template("""
DROP TABLE IF EXISTS ${customer_id}_users.journal;
CREATE TABLE  IF NOT EXISTS ${customer_id}_users.journal (
    lang VARCHAR(12) NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    ts TIMESTAMP,
    dialogue_id VARCHAR(100),
    step varchar(6),
    tag VARCHAR(100),                          
    times INT,
    mark FLOAT,
    PRIMARY KEY (lang,user_id, ts)
);
""")

# Template for user_vocab table
user_vocab_table = Template("""
DROP TABLE IF EXISTS ${customer_id}_users.user_vocab;
CREATE TABLE  IF NOT EXISTS ${customer_id}_users.user_vocab (
      lang VARCHAR(12) NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    customer_id VARCHAR(100) DEFAULT 'polyglots',
    last_mode VARCHAR(100) DEFAULT '',
    level INT,
    mark FLOAT,
    times INT,
    first_time TIMESTAMP DEFAULT NOW(),
    last_time TIMESTAMP,
    last_step VARCHAR(100),
    last_tag VARCHAR(100),
    current_practice_type VARCHAR(100) DEFAULT '', 
    current_practice_id VARCHAR(100) DEFAULT '',
    auto_play BOOLEAN DEFAULT TRUE,
    show_text BOOLEAN DEFAULT FALSE,
    reverse_mode BOOLEAN DEFAULT FALSE,
    evaluate_mode BOOLEAN DEFAULT FALSE,
    evaluate_count int DEFAULT 10,
    configs JSONB, 
    PRIMARY KEY ( lang, user_id)
);
""")


user_auth_table = Template("""
DROP TABLE IF EXISTS ${customer_id}_users.users;
CREATE TABLE  IF NOT EXISTS ${customer_id}_users.users (
    customer_id VARCHAR(100) NOT NULL default 'polyglots',
    email VARCHAR(200) NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    lang VARCHAR(12)  default '',
    to_lang VARCHAR(12) default '',
    last_login TIMESTAMP DEFAULT NOW(),
    first_login TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (customer_id, email, user_id)
);
""")


achievement_table = Template("""
DROP TABLE IF EXISTS ${customer_id}_users.achievement;
CREATE TABLE  IF NOT EXISTS ${customer_id}_users.achievement (
    user_id VARCHAR(100) NOT NULL,
    lang VARCHAR(12)  default '',
    granularity VARCHAR(12)  default 'day',
    ts TIMESTAMP DEFAULT NOW(),
    achievement_type CHAR(1) NOT NULL,
    count int default 0,                                                                         
    PRIMARY KEY (lang, granularity, achievement_type, user_id, ts)
);
""")



user_words_table = Template("""
    DROP TABLE IF EXISTS ${customer_id}_users.user_words;
    CREATE TABLE  IF NOT EXISTS ${customer_id}_users.user_words (
                    lang varchar(10) NOT NULL,
                    user_id varchar(50) NOT NULL,
                    word varchar(100) NOT NULL,
                    mark float8 DEFAULT 0.0 NULL,
                    times int4 DEFAULT 0 NULL,
                    first_time timestamp DEFAULT now() NULL,
                    last_time timestamp DEFAULT now() NULL,
                    CONSTRAINT user_words_pkey PRIMARY KEY (lang, user_id, word)
    );
""")



# Template for user_vocab table
# DELETE:
# user_vocab_table = Template("""
# DROP TABLE IF EXISTS ${customer_id}_users.practice;
# CREATE TABLE  IF NOT EXISTS ${customer_id}_users.practice (
#     lang CHAR(8) NOT NULL,
#     user_id VARCHAR(100) NOT NULL,
#     practice_type VARCHAR(1) NOT NULL,
#     practice_id VARCHAR(1) NOT NULL,
#     first_time TIMESTAMP DEFAULT NOW(),
#     last_time TIMESTAMP,
#     mark FLOAT,
#     times INT,
#     PRIMARY KEY (lang, user_id, practice_type, practice_id)
# );
# """)




TABLE_TEMPLATES = [
    user_vocab_table,
    user_content_table,
    user_journal_table,
    user_words_table,
]