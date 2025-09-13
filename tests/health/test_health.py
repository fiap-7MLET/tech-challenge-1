
def test_health_endpoint(client):
    response = client.get(f"/api/v1/health/")
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data["status"] == "ok"
    assert data["database"] == "up"
