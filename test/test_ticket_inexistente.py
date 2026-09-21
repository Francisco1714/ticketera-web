def test_ticket_inexistente(client):
    response = client.get("/api/v1/tickets/TK-00000000-9999")

    assert response.status_code == 404