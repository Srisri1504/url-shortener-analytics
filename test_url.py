from fastapi.testclient import TestClient
from main import app
from database import init_db

init_db()
client = TestClient(app)

def test_shorten_and_analytics():
    response = client.post("/api/shorten", json={"url": "https://python.org", "custom_alias": "pyhome"})
    assert response.status_code == 200
    data = response.json()
    assert data["short_code"] == "pyhome"

    redirect_res = client.get("/pyhome", follow_redirects=False)
    assert redirect_res.status_code == 307
    assert redirect_res.headers["location"] == "https://python.org/"

    stats_res = client.get("/api/stats/pyhome").json()
    assert stats_res["total_clicks"] >= 1
