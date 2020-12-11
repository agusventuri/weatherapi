import pytest
from weatherapi import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_empty_city(client):
    rv = client.get("/weather?city=&country=co")
    assert rv.json["cod"] == "400"


def test_empty_country(client):
    rv = client.get("/weather?city=valledupar&country=")
    assert rv.json["cod"] == "400"


def test_no_city(client):
    rv = client.get("/weather?country=co")
    assert rv.json["cod"] == "400"


def test_no_country(client):
    rv = client.get("/weather?city=valledupar")
    assert rv.json["cod"] == "400"


def test_no_data(client):
    rv = client.get("/weather")
    assert rv.json["cod"] == "400"


def test_country_not_lowercase(client):
    rv = client.get("/weather?city=valledupar&country=cO")
    assert rv.json["cod"] == "400"


def test_country_less_than_2_chars(client):
    rv = client.get("/weather?city=valledupar&country=c")
    assert rv.json["cod"] == "400"


def test_country_more_than_2_chars(client):
    rv = client.get("/weather?city=valledupar&country=col")
    assert rv.json["cod"] == "400"
