def test_user_token(client):
    response = client.post("/v1/auth/user", data={"username": "john", "password": "", "grant_type": "password"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_staff_token(client):
    response = client.post("/v1/auth/staff", data={"username": "admin", "password": "", "grant_type": "password"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
