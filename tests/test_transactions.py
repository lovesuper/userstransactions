def test_create_transaction(client):
    response = client.post("/v1/auth/staff", data={"username": "admin", "password": "", "grant_type": "password"})
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "data": {
            "type": "transaction",
            "attributes": {
                "user_id": "d8f0fe9a-68e5-4dad-9241-5a2382ece4d7",
                "amount": 1,
                "operation_type": "accrual"
            }
        }
    }
    response = client.post("/v1/transactions", json=payload, headers=headers)
    assert response.status_code in (200, 400)
