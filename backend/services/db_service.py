from http.client import responses

from flask.cli import load_dotenv
from sqlalchemy import create_engine, text
import os
import dotenv

load_dotenv()
engine = create_engine(os.getenv("DB_CONNECTION_STRING"))

#----- URL -----
def add_url(url: str):
    with engine.connect() as connection:
        connection.execute(text(
            'INSERT INTO URLS (url) VALUES (:url);'),
            parameters={'url': url}
        )
        connection.commit()
    return

def remove_url(url: str):
    with engine.connect() as connection:
        connection.execute(text(
            'DELETE FROM URLS WHERE url = :url;'),
            parameters = {'url': url}
        )
        connection.commit()
    return

def find_url_by_name(url: str):
    with engine.connect() as connection:
        sql_response = connection.execute(text(
            'SELECT * FROM URLS WHERE url = :url;'),
            parameters={'url': url}
        )

        rows = sql_response.fetchall()
        if len(rows) != 0:
            return rows
        else:
            return None

def find_url_by_id(url_id: int):
    with engine.connect() as connection:
        sql_response = connection.execute(text(
            'SELECT * FROM URLS WHERE id = :id'),
            parameters={'id': url_id}
        )

        rows = sql_response.fetchall()
        if len(rows) != 0:
            return rows[0][1]
        else:
            return None

def update_url_timestamp(url_id: int):
    with engine.connect() as connection:
        connection.execute(text(
            'UPDATE URLS SET created_at = NOW() WHERE id = :id;'),
            parameters={'id': url_id}
        )

def find_urls_junger_then_one_day():
    with engine.connect() as connection:
        sql_response = connection.execute(text(
            'SELECT * FROM URLS WHERE urls.created_at > NOW() - INTERVAL \'1 day\''),
        )

    rows = sql_response.fetchall()
    if len(rows) != 0:
        return rows
    else:
        return None

def find_urls_junger_then_one_day_filtered():
    with engine.connect() as connection:
        sql_response = connection.execute(text(
            'SELECT url FROM URLS WHERE urls.created_at > NOW() - INTERVAL \'1 day\''),
        )

    rows = sql_response.fetchall()
    if len(rows) != 0:
        return rows
    else:
        return None

def find_urls_older_then_one_day():
    with engine.connect() as connection:
        sql_response = connection.execute(text(
            'SELECT * FROM URLS WHERE urls.created_at < NOW() - INTERVAL \'1 day\''),
        )

    rows = sql_response.fetchall()
    if len(rows) != 0:
        return rows
    else:
        return None

#----- WORD -----

def add_word(word: str):
    with engine.connect() as connection:
        connection.execute(text(
            'INSERT INTO WORDS (word) VALUES (:word);'),
            parameters={'word': word}
        )
        connection.commit()
    return

def remove_word(word: str):
    with engine.connect() as connection:
        connection.execute(text(
            'DELETE FROM WORDS WHERE word = :word;'),
            parameters = {'word': word}
        )
        connection.commit()
    return

def find_word_by_name(word: str):
    with engine.connect() as connection:
        sql_response = connection.execute(text(
            'SELECT * FROM WORDS WHERE word = :word;'),
            parameters={'word': word}
        )

        rows = sql_response.fetchall()
        if len(rows) != 0:
            return rows[0][0]
        else:
            return None

#----- LINKS -----

def add_link(word_id: int, url_id: int):
    with engine.connect() as connection:
        connection.execute(text(
            'INSERT INTO WORD_LINKS (word_id, url_id) VALUES (:word_id, :url_id);'),
            parameters={'word_id': word_id, 'url_id': url_id}
        )
        connection.commit()
    return

def remove_link(word_id: int):
    with engine.connect() as connection:
        connection.execute(text(
            'DELETE FROM WORD_LINKS WHERE word_id = :word_id;'),
            parameters={'word_id': word_id}
        )
        connection.commit()
    return

def find_link_by_word_id(word_id: int):
    with engine.connect() as connection:
        sql_response = connection.execute(text(
            'SELECT * FROM WORD_LINKS WHERE word_id = :word_id;'),
            parameters={'word_id': word_id}
        )
        connection.commit()

        rows = sql_response.fetchall()[0]
        if len(rows) != 0:
            return rows
        else:
            return None

#----- More -----
def find_url_containing_word(word_id:int):
    response = find_link_by_word_id(word_id)

    return response
