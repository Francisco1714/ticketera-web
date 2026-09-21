def test_actualizar_parcial(client):
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

    response = client.patch(
        f"/api/v1/tickets/{ticket_id}",
        json={"estado": "en progreso", "tecnico_asignado": "María López"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["estado"] == "en progreso"
    assert data["tecnico_asignado"] == "María López"
    assert data["prioridad"] == "media"  # no debe cambiarse