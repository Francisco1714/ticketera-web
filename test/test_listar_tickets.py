def test_listar_tickets(client):
    payload = {
        "solicitante": {
            "rut":"12345678-9",
            "nombre":"Juan Pérez",
            "telefono":"+56912345678",
            "email":"juan@ejemplo.com",
            "area":"Operaciones",
            "cargo":"Analista",
        },
        "descripcion":"No enciende el equipo del escritorio 5",
        "categoria":"Hardware",
        "prioridad":"media",
    }
    client.post("/api/v1/tickets", json=payload)
    client.post("/api/v1/tickets", json=payload)

    response = client.get("/api/v1/tickets")

    assert response.status_code == 200
    data = response.json()
    assert  len(data) == 2
    assert data[0]["ticket_id"].startswith("TK-")