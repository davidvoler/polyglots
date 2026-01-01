from string import Template



quiz_table = Template(
    """
    -- DROP TABLE IF EXISTS ${customer_id}_quiz.parts;
    CREATE TABLE  IF NOT EXISTS ${customer_id}_quiz.parts (
        lang VARCHAR(12) NOT NULL,
        part_id VARCHAR(300) NOT NULL,
        text VARCHAR(400),
        recording VARCHAR(255),
        words VARCHAR(100)[],
        options VARCHAR(400)[],
        level INT,
        step INT,
        PRIMARY KEY (lang, part_id)
    );
    """
)

dialogue_table = Template(
    """
    DROP TABLE IF EXISTS ${customer_id}_quiz.dialogue;
    CREATE TABLE  IF NOT EXISTS ${customer_id}_quiz.dialogue (
        lang VARCHAR(12) NOT NULL,
        dialogue_id VARCHAR(300) NOT NULL,
        text TEXT,
        words VARCHAR(100)[],
        parts VARCHAR(100)[],
        phrases VARCHAR(100)[],
        level INT,
        step INT,
        tag VARCHAR(100),
        PRIMARY KEY (lang, dialogue_id)
    );
    """
)

dialogue_lines_table = Template(
    """
    DROP TABLE IF EXISTS ${customer_id}_quiz.dialogue_line;
    CREATE TABLE  IF NOT EXISTS ${customer_id}_quiz.dialogue_line (
        lang VARCHAR(12) NOT NULL,
        dialogue_line VARCHAR(300) NOT NULL,
        dialogue_id VARCHAR(300) NOT NULL,
        text VARCHAR(400),
        words VARCHAR(100)[],
        options VARCHAR(400)[],
        recording VARCHAR(255),
        line_no INT,
        tag VARCHAR(100),
        step VARCHAR(100),
        PRIMARY KEY (lang, dialogue_line)
    );

    """
)   

tags_table = Template(
    """
    DROP TABLE IF EXISTS ${customer_id}_quiz.tags;
    CREATE TABLE  IF NOT EXISTS ${customer_id}_quiz.tags (
        lang VARCHAR(12) NOT NULL,
        tag_id VARCHAR(100) NOT NULL,
        tag VARCHAR(200),
        dialogues VARCHAR(100)[],
        parts VARCHAR(400)[],
        level INT,
        PRIMARY KEY ( lang, tag_id)
    );
    """
)
steps_table = Template(
    """
    DROP TABLE IF EXISTS ${customer_id}_quiz.steps;
    CREATE TABLE  IF NOT EXISTS ${customer_id}_quiz.steps (
        lang VARCHAR(12) NOT NULL,
        step_id VARCHAR(100) NOT NULL,
        step INT,
        level INT,
        words VARCHAR(100)[],
        parts VARCHAR(400)[],
    	dialogues VARCHAR(400) NULL,
	    structure VARCHAR(400) NULL,
	    lines VARCHAR(400) NULL,
        PRIMARY KEY (lang, step_id)
    );
    """
)

words_table = Template(
    """
    DROP TABLE IF EXISTS ${customer_id}_quiz.words;
    CREATE TABLE  IF NOT EXISTS  ${customer_id}_quiz.words; (
        id VARCHAR(150) NOT NULL,
        lang VARCHAR(12) NOT NULL,
        word VARCHAR(150) NOT NULL,
        level INT,
        group INT,
        PRIMARY KEY (id, lang)
    );
    """
)


structure_table = Template("""
DROP TABLE IF EXISTS ${customer_id}_content.structure;
CREATE TABLE  IF NOT EXISTS ${customer_id}_content.structure (
    lang VARCHAR(12) NOT NULL,
    struct_type VARCHAR(10) NOT NULL,
    struct VARCHAR(100) NOT NULL,
    step INT,
    root VARCHAR(100),
    ids VARCHAR(400)[],
    ids_count INT,  
    PRIMARY KEY (lang, struct_type, struct)
);
""")
## indexes 

parts_quiz_index = Template(
    """
    CREATE INDEX quiz_parts_words ON ${customer_id}_quiz.parts USING GIN (words);
    """
)

TABLE_TEMPLATES = [
    quiz_table,
    dialogue_table,
    dialogue_lines_table,
    tags_table,
    steps_table,
    parts_quiz_index,
]