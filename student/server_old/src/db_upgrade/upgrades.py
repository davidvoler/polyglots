from utils.db import get_pg_conn, run_query


def create_user_words():
    """
    Create user words table if it doesn't exist.
    """
    run_query("""
            CREATE TABLE IF NOT EXISTS polyglots_users.user_words (
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


def add_dialogues_in_dialogue_lines():
   

    sql = f"""
    select * from polyglots_quiz.step
    """