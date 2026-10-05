import pytest
from fastapi.testclient import TestClient
from mongoengine import connect, disconnect
from api.main import app
from api.models.ticket import Comentario, HistorialCambio, Ticket

@pytest.fixture()
def client():
    disconnect(alias="default")
    connect(
        db="ticketera_test",
        host="localhost",
        port=27017,
        alias="default",
    )
    yield TestClient(app)
    Ticket.drop_collection()
    disconnect(alias="default")


@pytest.fixture()
def ticket_con_comentario(client):
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
    ticket_id = client.post("/api/v1/tickets", json=payload).json()["ticket_id"]
    t = Ticket.objects.get(ticket_id=ticket_id)
    t.comentarios.append(Comentario(autor="tecnico", texto="revisando"))
    t.historial_cambios.append(
        HistorialCambio(
            estado_anterior="abierto",
            estado_nuevo="cerrado",
            cambiado_por="tecnico",
        )
    )
    t.save()
    return ticket_id