from backend.services import db_service

def get_word_id_by_word(word: str):
    return db_service.find_word_by_name(word.lower())[0][0]

def get_urls_containing_word(word_id: int):
    try:
        url_ids = db_service.find_url_containing_word(word_id)[0]
        urls = []

        for url_id in url_ids:
            urls.append(db_service.find_url_by_id(url_id)[0])

        return urls
    except Exception as e:
        return e

def search_urls_by_therm(search_therm: str):
    word_id = get_word_id_by_word(search_therm)
    urls_res = get_urls_containing_word(word_id)
    urls = []

    for url in urls_res:
        urls.append(url[1])

    return urls
