from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class Solicitante(BaseModel):
    """Datos de quien genera la solicitud"""
    rut: str = Field(..., description="RUT del solicitante")
    nombre: str = Field(..., description="Nombre completo")
    telefono: str = Field(..., description="Teléfono de contacto")
    email: str = Field(..., description="Correo electrónico")
    area: str = Field(..., description="Área o departamento")
    cargo: str = Field(..., description="Cargo que desempeña")

class Comentario(BaseModel):
    """Comentario agregado a un ticket"""
    autor: str = Field(..., description="Quién comenta")
    texto: str = Field(..., description="Contenido del comentario")
    fecha: datetime = Field(default_factory=datetime.now)

class HistorialCambio(BaseModel):
    """Registro de cambio de estado"""
    estado_anterior: str
    estado_nuevo: str
    cambiado_por: str
    fecha: datetime = Field(default_factory=datetime.now)
    observacion: Optional[str] = None

class TicketCreate(BaseModel):
    """Esquema para crear ticket"""
    solicitante: Solicitante
    descripcion: str = Field(..., min_length=10)
    categoria: str
    prioridad: str = "media"

class TicketResponse(BaseModel):
    """Esquema de respuesta de un ticket"""
    ticket_id: str
    solicitante: Solicitante
    descripcion: str
    categoria: str
    prioridad: str
    estado: str
    tecnico_asignado: Optional[str] = None
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    fecha_resolucion: Optional[datetime] = None
    comentarios: List[Comentario] = []
    historial_cambios: List[HistorialCambio] = []

class TicketUpdate(BaseModel):
    """Esquema  para actualizar ticket"""
    solicitante:Solicitante
    descripcion:str = Field(..., min_length=10)
    categoria:str
    prioridad:str
    estado:Optional[str] = None

class TicketPatch(BaseModel):
    """Esquema para actualizacion parcial"""
    estado: Optional[str] = None
    prioridad: Optional[str] = None
    tecnico_asignado: Optional[str] = None