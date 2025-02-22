def test_create_user(client):
    payload = {
        "data": {
            "type": "users",
            "attributes": {
                "username": "testuser",
                "email": "test@example.com",
                "first_name": "Test",
                "last_name": "User",
                "city": "TestCity",
                "country": "TestCountry"
            }
        }
    }
    response = client.post("/v1/users", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["data"]["attributes"]["username"] == "testuser"


def test_create_user_invalid_jsonapi(client):
    payload = {
        "type": "users",
        "attributes": {
            "username": "testuser2",
            "email": "test2@example.com",
            "first_name": "Test2",
            "last_name": "User2",
            "city": "TestCity",
            "country": "TestCountry"
        }
    }
    response = client.post("/v1/users", json=payload)
    assert response.status_code == 422
