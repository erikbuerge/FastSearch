from http.client import responses

from sqlalchemy import create_engine, text

engine = create_engine("postgresql://santa:claus@localhost:5432/postgres")

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
            return rows
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

        rows = sql_response.fetchall()
        if len(rows) != 0:
            return rows
        else:
            return None

#----- More -----
def find_url_containing_word(word_id:int):
    response = find_link_by_word_id(word_id)

    return response
