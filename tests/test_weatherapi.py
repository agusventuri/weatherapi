import pytest
from weatherapi import create_app


# created client that will run the tests
@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_empty_city(client):
    rv = client.get("/weather?city=&country=co")
    assert rv.status_code == 400


def test_empty_country(client):
    rv = client.get("/weather?city=valledupar&country=")
    assert rv.status_code == 400


def test_no_city(client):
    rv = client.get("/weather?country=co")
    assert rv.status_code == 400


def test_no_country(client):
    rv = client.get("/weather?city=valledupar")
    assert rv.status_code == 400


def test_no_data(client):
    rv = client.get("/weather")
    assert rv.status_code == 400


def test_country_not_lowercase(client):
    rv = client.get("/weather?city=valledupar&country=cO")
    assert rv.status_code == 400


def test_country_less_than_2_chars(client):
    rv = client.get("/weather?city=valledupar&country=c")
    assert rv.status_code == 400


def test_country_more_than_2_chars(client):
    rv = client.get("/weather?city=valledupar&country=col")
    assert rv.status_code == 400


def test_ok(client):
    rv = client.get("/weather?city=valledupar&country=co")
    assert rv.status_code == 200
