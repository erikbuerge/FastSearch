import pytest
from backend.services import db_service


@pytest.mark.order(1)
def test_db_connection():
    assert True

@pytest.mark.order(2)
def test_db_insert():
    db_service.add_word("pt-testword-1")

@pytest.mark.order(3)
def test_db_find_by_name():
    db_service.find_url_by_name("pt-testword-1")

@pytest.mark.order(4)
def test_db_delete():
    db_service.remove_url("pt-testword-1")