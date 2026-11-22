from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["platform"] == "FindZora"

def test_create_and_list_event():
    # Create event
    payload = {
        "name": "MCA Graduation Gala 2026",
        "description": "Annual MCA batch celebration and award ceremony.",
        "organizer_name": "Arshad Pasha",
        "organizer_email": "arshad@example.com",
        "retention_days": 15
    }
    create_res = client.post("/api/events", json=payload)
    assert create_res.status_code == 201
    event_id = create_res.json()["id"]

    # List events
    list_res = client.get("/api/events")
    assert list_res.status_code == 200
    events = list_res.json()
    assert any(e["id"] == event_id for e in events)

    # Consent recording
    consent_res = client.post(f"/api/events/{event_id}/consent", json={"attendee_name": "Test Attendee"})
    assert consent_res.status_code == 200
    assert consent_res.json()["status"] == "consent_recorded"

    # Delete event
    del_res = client.delete(f"/api/events/{event_id}")
    assert del_res.status_code == 200
