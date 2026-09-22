from datetime import datetime
from mongoengine import (
    Document,
    StringField,
    DateTimeField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    ListField,
)

class Solicitante(EmbeddedDocument):
    """Datos del solicitante (embebido en el ticket)"""
    rut = StringField(required=True)
    nombre = StringField(required=True)
    telefono = StringField(required=True)
    email = StringField(required=True)
    area = StringField(required=True)
    cargo = StringField(required=True)

class Comentario(EmbeddedDocument):
    """Comentario en un ticket"""
    autor = StringField(required=True)
    texto = StringField(required=True)
    fecha = DateTimeField(default=datetime.now)

class HistorialCambio(EmbeddedDocument):
    """Registro de cambio de estado"""
    estado_anterior = StringField(required=True)
    estado_nuevo = StringField(required=True)
    cambiado_por = StringField(required=True)
    fecha = DateTimeField(default=datetime.now)
    observacion = StringField()

class Ticket(Document):
    """Ticket principal de ticket MongoDB"""
    ticket_id = StringField(required=True, unique=True)
    solicitante = EmbeddedDocumentField(Solicitante, required=True)
    descripcion = StringField(required=True)
    categoria = StringField(required=True)
    prioridad = StringField(default="media")
    estado = StringField(default="abierto")
    tecnico_asignado = StringField()
    fecha_creacion = DateTimeField(default=datetime.now)
    fecha_actualizacion = DateTimeField(default=datetime.now)
    fecha_resolucion = DateTimeField()
    comentarios = ListField(EmbeddedDocumentField(Comentario))
    historial_cambios = ListField(EmbeddedDocumentField(HistorialCambio))

    meta = {
        'collection':'tickets', # Nombre de la coleccion de MongoDB
        'ordering':['-fecha_creacion'] # Ordenar por fecha descendente
    }