from app import app


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    # Enhanced health payload required by the student exercise.
    assert "application_version" in data
    assert "model_version" in data


def test_prediction():
    client = app.test_client()
    response = client.post("/predict", json={"value": 5})
    assert response.status_code == 200
    data = response.get_json()
    assert data["prediction"] == 10
