import pytest
from fastapi.testclient import TestClient
from main import app

IMAGE_URL = "https://drive.google.com/uc?export=view&id=1frcH2XKsTqgE66AJaazRkb-NMS7lhJ2V"

@pytest.fixture
def client():
    return TestClient(app)


def test_items_missing_no_image(client):
    resp = client.post("/submit-ticket", json={
        "user_id": "u1",
        "order_id": "o1",
        "problem_text": "The fries and coke were missing from my order",
        "image_url": None,
        "restaurant_name": "Testaurant"
    })
    data = resp.json()
    assert data["reply_tag"] == "image_required"
    assert data["status"] == "Pending"


def test_items_missing_image_match(monkeypatch, client):
    # Mock extractor to return matching items
    monkeypatch.setattr("image_extractor.extract_image_text", lambda url: ["fries", "coke"])
    resp = client.post("/submit-ticket", json={
        "user_id": "u2",
        "order_id": "o2",
        "problem_text": "The fries and coke were missing from my order",
        "image_url": IMAGE_URL,
        "restaurant_name": "Testaurant"
    })
    data = resp.json()
    assert data["reply_tag"] == "image_verification_required"
    assert data["status"] == "Pending"


def test_items_missing_image_mismatch(monkeypatch, client):
    # Mock extractor to return non-matching items
    monkeypatch.setattr("image_extractor.extract_image_text", lambda url: ["pizza"])
    resp = client.post("/submit-ticket", json={
        "user_id": "u3",
        "order_id": "o3",
        "problem_text": "The fries and coke were missing from my order",
        "image_url": IMAGE_URL,
        "restaurant_name": "Testaurant"
    })
    data = resp.json()
    assert data["reply_tag"] == "items_price_refund_initiated"
    assert data["status"] == "Resolved"


def test_items_missing_image_empty(monkeypatch, client):
    # Mock extractor to return empty list
    monkeypatch.setattr("image_extractor.extract_image_text", lambda url: [])
    resp = client.post("/submit-ticket", json={
        "user_id": "u4",
        "order_id": "o4",
        "problem_text": "The fries and coke were missing from my order",
        "image_url": IMAGE_URL,
        "restaurant_name": "Testaurant"
    })
    data = resp.json()
    assert data["reply_tag"] == "image_required"
    assert data["status"] == "Pending"
