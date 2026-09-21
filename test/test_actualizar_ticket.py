def test_actualizar_ticket(client):
    payload = {
        "solicitante": {
            "rut": "12345678-9",
            "nombre": "Juan Pérez",
            "telefono": "+56912345678",
            "email": "juan@ejemplo.com",
            "area": "Operaciones",
            "cargo": "Analista",
        },
        "descripcion": "No enciende el equipo del escritorio 5",
        "categoria": "Hardware",
        "prioridad": "media",
    }
    crear = client.post("/api/v1/tickets", json=payload)
    ticket_id = crear.json()["ticket_id"]

    update = {
        "solicitante": payload["solicitante"],
        "descripcion": "Equipo sin señal de video, revisado por técnico",
        "categoria": "Hardware",
        "prioridad": "alta",
    }
    response = client.put(f"/api/v1/tickets/{ticket_id}", json=update)

    assert response.status_code == 200
    data = response.json()
    assert data["prioridad"] == "alta"
    assert data["descripcion"] == "Equipo sin señal de video, revisado por técnico"