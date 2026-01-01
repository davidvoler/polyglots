

from string import Template

# Template for prompts table
prompts_table = Template("""
       DROP TABLE IF EXISTS ${customer_id}_content.prompts;
CREATE TABLE  IF NOT EXISTS ${customer_id}_content.prompts (
    lang VARCHAR(12) NOT NULL,
    user_id VARCHAR(200) NOT NULL,
    prompt_id VARCHAR(400) NOT NULL,
    prompt TEXT,
    model VARCHAR(100),
    num_res INT,
    PRIMARY KEY (lang, user_id, prompt_id)
);
""")

# Template for sentences table
sentences_table = Template("""
    DROP TABLE IF EXISTS  ${customer_id}_content.sentences;
CREATE TABLE  IF NOT EXISTS ${customer_id}_content.sentences (
    lang VARCHAR(12) NOT NULL,
    id VARCHAR(400) NOT NULL,                       
    text VARCHAR(400),
    level INT,
    recording VARCHAR(255),
    words VARCHAR(100)[],
    part_type CHAR(1), -- l - line, s - sentence, p - phrase, w - word
    model VARCHAR(100),
    PRIMARY KEY (lang, id)
);
""")

# Template for unique_sentences table
unique_sentences_table = Template("""
      DROP TABLE IF EXISTS ${customer_id}_content.unique_sentences;
CREATE TABLE  IF NOT EXISTS ${customer_id}_content.unique_sentences (
    lang VARCHAR(12) NOT NULL,
    id VARCHAR(400) NOT NULL,
    text VARCHAR(400),
    PRIMARY KEY (lang, id)
);
""")

# Template for unique_parts table
unique_parts_table = Template("""
    DROP TABLE IF EXISTS ${customer_id}_content.unique_parts;
    CREATE TABLE  IF NOT EXISTS ${customer_id}_content.unique_parts (
    lang VARCHAR(12) NOT NULL,
    part_id VARCHAR(400) NOT NULL,
    text VARCHAR(400),
    level INT,
    step INT,
    tag VARCHAR(100),
    recording VARCHAR(255),
    words VARCHAR(100)[],
    part_type CHAR(1), -- l - line, s - sentence, p - phrase, w - word
    model VARCHAR(100),
    structure VARCHAR(100),
    PRIMARY KEY (lang, part_id)
);
""")

# Template for recording table
recording_table = Template("""
    DROP TABLE IF EXISTS ${customer_id}_content.recording;
CREATE TABLE  IF NOT EXISTS ${customer_id}_content.recording (
    lang VARCHAR(12) NOT NULL,
    part_id VARCHAR(400) NOT NULL,
    voice_type CHAR(1), -- f - female, m - male, c - child
    voice VARCHAR(255),
    text VARCHAR(400),
    recording VARCHAR(255),
    PRIMARY KEY (lang, part_id, voice_type, voice)
);
""")

# Template for dialogue table
dialogue_table = Template("""
    DROP TABLE IF EXISTS ${customer_id}_content.dialogue;
CREATE TABLE  IF NOT EXISTS ${customer_id}_content.dialogue (
    lang VARCHAR(12) NOT NULL,
    dialogue_id VARCHAR(400) NOT NULL,
    text TEXT,
    words VARCHAR(100)[],
    parts VARCHAR(100)[],
    phrases VARCHAR(100)[],
    level INT,
    step INT,
    tag VARCHAR(100),
    PRIMARY KEY (dialogue_id, lang)
);
""")

# Template for dialogue_line table
dialogue_line_table = Template("""
    DROP TABLE IF EXISTS ${customer_id}_content.dialogue_line;
CREATE TABLE  IF NOT EXISTS ${customer_id}_content.dialogue_line (
    lang VARCHAR(12) NOT NULL,
    dialogue_id VARCHAR(400) NOT NULL,
    dialogue_line INT,
    text VARCHAR(400),
    words VARCHAR(100)[],
    level INT,
    step INT,
    tag VARCHAR(100),
    PRIMARY KEY (lang, dialogue_id, dialogue_line)
);
""")

# Template for tags table
tags_table = Template("""
    DROP TABLE IF EXISTS ${customer_id}_content.tags;
CREATE TABLE  IF NOT EXISTS ${customer_id}_content.tags (
    lang VARCHAR(12) NOT NULL,
    tag_id VARCHAR(100) NOT NULL,
    tag VARCHAR(400),
    level INT,
    PRIMARY KEY (lang, tag_id)
);
""")

# Template for steps table
steps_table = Template("""
    DROP TABLE IF EXISTS ${customer_id}_content.steps;
CREATE TABLE  IF NOT EXISTS ${customer_id}_content.steps (
    step_id VARCHAR(100) NOT NULL,
    lang VARCHAR(12) NOT NULL,
    level INT,
    PRIMARY KEY ( lang, step_id)
);
""")


# prepared sentences 
prepared_sentences_table = Template("""
    DROP TABLE IF EXISTS ${customer_id}_content.prepared_sentences;
    CREATE TABLE IF NOT EXISTS  ${customer_id}_content.prepared_sentences (
    id VARCHAR(255) NOT NULL,
    lang VARCHAR(12) NOT NULL,
    sentence VARCHAR(255),
    subject VARCHAR(100),
    all_words VARCHAR(100) [],
    c_count INTEGER,
    first VARCHAR(100) ,
    first_c VARCHAR(100) ,
    last_c VARCHAR(100) ,
    pos VARCHAR(100) [],
    propn VARCHAR(100) [],
    root VARCHAR(100) ,
    stop_words VARCHAR(100) [],
    w_count INTEGER,
    words VARCHAR(100) [],
    o_count INTEGER,
    options VARCHAR(255) [],
    structure3 VARCHAR(100),
    structure4 VARCHAR(100),
    structure_root VARCHAR(100),
    PRIMARY KEY (lang, id)
);
                                   
""")


    
structure_table = Template("""
    DROP TABLE IF EXISTS ${customer_id}_content.structure;
CREATE TABLE  IF NOT EXISTS ${customer_id}_content.structure (
    lang VARCHAR(12) NOT NULL,
    struct_type VARCHAR(10) NOT NULL,
    struct VARCHAR(100) NOT NULL,
    ids VARCHAR(400)[],
    ids_count INT,  
    PRIMARY KEY (lang, struct_type, struct)
);
""")


TABLE_TEMPLATES = [
    prompts_table,
    sentences_table,
    unique_sentences_table,
    unique_parts_table,
    recording_table,
    dialogue_table,
    dialogue_line_table,
    tags_table,
    steps_table,
    prepared_sentences_table,
]