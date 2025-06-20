from . import db_service

def search_by_therm(search_therm: str):
    word_id: int = db_service.find_word_by_name(search_therm.lower())

    if word_id is None:
        return "Search term not found"

    url_ids = db_service.find_link_by_word_id(word_id)

    if url_ids is None:
        return "No URLs for the search term"

    urls = []
    for url_id in url_ids:
        urls.append(db_service.find_url_by_id(url_id))

    return urls