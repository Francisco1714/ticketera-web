import pytest
from fastapi.testclient import TestClient
from mongoengine import connect, disconnect

from api.main import app 

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
    from api.models.ticket import Ticket
    Ticket.drop_collection()
    disconnect(alias="default")