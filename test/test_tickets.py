def test_crear_ticket(client):
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
    response = client.post("/api/v1/tickets", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["ticket_id"].startswith("TK-")
    assert data["estado"] == "abierto"