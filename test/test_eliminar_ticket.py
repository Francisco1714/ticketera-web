def test_eliminar_ticket(client):
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

    response = client.delete(f"/api/v1/tickets/{ticket_id}")

    assert response.status_code == 204

    # Verificar que ya no existe
    get = client.get(f"/api/v1/tickets/{ticket_id}")
    assert get.status_code == 404