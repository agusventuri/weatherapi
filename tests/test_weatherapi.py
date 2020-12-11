import pytest
from weatherapi import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_no_city(client):
    rv = client.get("/weather?city=&country=co")
    assert rv.json["cod"] == "400"


def test_no_country(client):
    rv = client.get("/weather?city=valledupar&country=")
    assert rv.json["cod"] == "400"


def test_no_data(client):
    rv = client.get("/weather")
    assert rv.json["cod"] == "400"
