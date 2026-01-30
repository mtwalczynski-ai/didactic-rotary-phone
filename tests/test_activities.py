from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Expect activities dict with at least one known activity
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "test_user@example.com"

    # Ensure email is not already signed up; if it is, remove first
    activities = client.get("/activities").json()
    if email in activities[activity]["participants"]:
        del_resp = client.delete(f"/activities/{activity}/participants?email={email}")
        assert del_resp.status_code == 200

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert resp.json()["message"]

    # Verify participant was added
    activities_after = client.get("/activities").json()
    assert email in activities_after[activity]["participants"]

    # Now unregister
    del_resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert del_resp.status_code == 200
    assert del_resp.json()["message"]

    # Verify removed
    activities_final = client.get("/activities").json()
    assert email not in activities_final[activity]["participants"]
