import os
from fastapi import FastAPI
from mongoengine import connect
from datetime import datetime
from .schemas.ticket import TicketCreate, TicketResponse, TicketUpdate, TicketPatch
from .models.ticket import Ticket, Solicitante

app = FastAPI(title="Ticketera API", version="0.1.0")


@app.on_event("startup")
def startup_db():
    connect(
        db=os.getenv('MONGO_DB', 'ticketera'),
        host=os.getenv('MONGO_HOST', 'localhost'),
        port=int(os.getenv('MONGO_PORT', '27017')),
    )


@app.on_event("shutdown")
def shutdown_db():
    from mongoengine import disconnect
    disconnect()


@app.get("/")
def root():
    return {"message": "API de Soporte TI"}

def  generar_ticket_id():
    fecha = datetime.now().strftime("%Y%m%d")
    cantidad = Ticket.objects.count() + 1
    return f"TK-{fecha}-{cantidad:04d}"

@app.post("/api/v1/tickets", response_model=TicketResponse, status_code=201)
def crear_ticket(ticket:  TicketCreate):
    solicitante = Solicitante(
        rut=ticket.solicitante.rut,
        nombre=ticket.solicitante.nombre,
        telefono=ticket.solicitante.telefono,
        email=ticket.solicitante.email,
        area=ticket.solicitante.area,
        cargo=ticket.solicitante.cargo,
    )

    nuevo_ticket = Ticket(
        ticket_id=generar_ticket_id(),
        solicitante=solicitante,
        descripcion=ticket.descripcion,
        categoria=ticket.categoria,
        prioridad=ticket.prioridad,
        estado="abierto",
        fecha_creacion=datetime.now(),
        fecha_actualizacion=datetime.now(),
    )

    nuevo_ticket.save()

    return TicketResponse(
        ticket_id=nuevo_ticket.ticket_id,
        solicitante=ticket.solicitante,
        descripcion=nuevo_ticket.descripcion,
        categoria=nuevo_ticket.categoria,
        prioridad=nuevo_ticket.prioridad,
        estado=nuevo_ticket.estado,
        fecha_creacion=nuevo_ticket.fecha_creacion,
        fecha_actualizacion=nuevo_ticket.fecha_actualizacion,
    )

@app.get("/api/v1/tickets", response_model=list[TicketResponse])
def listar_tickets():
    """Listar todos los tickets"""
    tickets = Ticket.objects.all()
    return[
        TicketResponse(
            ticket_id=t.ticket_id,
            solicitante={
                "rut":t.solicitante.rut,
                "nombre":t.solicitante.nombre,
                "telefono": t.solicitante.telefono,
                "email": t.solicitante.email,
                "area": t.solicitante.area,
                "cargo": t.solicitante.cargo
            },
            descripcion=t.descripcion,
            categoria=t.categoria,
            prioridad=t.prioridad,
            estado=t.estado,
            tecnico_asignado=t.tecnico_asignado,
            fecha_creacion=t.fecha_creacion,
            fecha_actualizacion=t.fecha_actualizacion,
            fecha_resolucion=t.fecha_resolucion,
            comentarios=[],
            historial_cambios=[]
        )
        for t in tickets 
    ]

@app.get("/api/v1/tickets/{ticket_id}", response_model=TicketResponse)
def obtener_ticket(ticket_id: str):
    """Obtener un ticket por su ID"""
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    
    return TicketResponse(
        ticket_id=ticket.ticket_id,
        solicitante={
            "rut": ticket.solicitante.rut,
            "nombre": ticket.solicitante.nombre,
            "telefono": ticket.solicitante.telefono,
            "email": ticket.solicitante.email,
            "area": ticket.solicitante.area,
            "cargo": ticket.solicitante.cargo
        },
        descripcion=ticket.descripcion,
        categoria=ticket.categoria,
        prioridad=ticket.prioridad,
        estado=ticket.estado,
        tecnico_asignado=ticket.tecnico_asignado,
        fecha_creacion=ticket.fecha_creacion,
        fecha_actualizacion=ticket.fecha_actualizacion,
        fecha_resolucion=ticket.fecha_resolucion,
        comentarios=[],
        historial_cambios=[]
    )

@app.put("/api/v1/tickets/{ticket_id}", response_model=TicketResponse)
def actualizar_ticket(ticket_id: str, datos: TicketUpdate):
    """Actualizar un ticket completo"""
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    
    ticket.solicitante.rut = datos.solicitante.rut
    ticket.solicitante.nombre = datos.solicitante.nombre
    ticket.solicitante.telefono = datos.solicitante.telefono
    ticket.solicitante.email = datos.solicitante.email
    ticket.solicitante.area = datos.solicitante.area
    ticket.solicitante.cargo = datos.solicitante.cargo
    ticket.descripcion = datos.descripcion
    ticket.categoria = datos.categoria
    ticket.prioridad = datos.prioridad
    ticket.fecha_actualizacion = datetime.now()
    
    ticket.save()
    
    return TicketResponse(
        ticket_id=ticket.ticket_id,
        solicitante={
            "rut": ticket.solicitante.rut,
            "nombre": ticket.solicitante.nombre,
            "telefono": ticket.solicitante.telefono,
            "email": ticket.solicitante.email,
            "area": ticket.solicitante.area,
            "cargo": ticket.solicitante.cargo
        },
        descripcion=ticket.descripcion,
        categoria=ticket.categoria,
        prioridad=ticket.prioridad,
        estado=ticket.estado,
        tecnico_asignado=ticket.tecnico_asignado,
        fecha_creacion=ticket.fecha_creacion,
        fecha_actualizacion=ticket.fecha_actualizacion,
        fecha_resolucion=ticket.fecha_resolucion,
        comentarios=[],
        historial_cambios=[]
    )

@app.patch("/api/v1/tickets/{ticket_id}", response_model=TicketResponse)
def actualizar_parcial_ticket(ticket_id: str, datos: TicketPatch):
    """Actualizar campos específicos de un ticket"""
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    
    if datos.estado is not None:
        ticket.estado = datos.estado
    if datos.prioridad is not None:
        ticket.prioridad = datos.prioridad
    if datos.tecnico_asignado is not None:
        ticket.tecnico_asignado = datos.tecnico_asignado
    
    ticket.fecha_actualizacion = datetime.now()
    ticket.save()
    
    return TicketResponse(
        ticket_id=ticket.ticket_id,
        solicitante={
            "rut": ticket.solicitante.rut,
            "nombre": ticket.solicitante.nombre,
            "telefono": ticket.solicitante.telefono,
            "email": ticket.solicitante.email,
            "area": ticket.solicitante.area,
            "cargo": ticket.solicitante.cargo
        },
        descripcion=ticket.descripcion,
        categoria=ticket.categoria,
        prioridad=ticket.prioridad,
        estado=ticket.estado,
        tecnico_asignado=ticket.tecnico_asignado,
        fecha_creacion=ticket.fecha_creacion,
        fecha_actualizacion=ticket.fecha_actualizacion,
        fecha_resolucion=ticket.fecha_resolucion,
        comentarios=[],
        historial_cambios=[]
    )

@app.delete("/api/v1/tickets/{ticket_id}", status_code=204)
def eliminar_ticket(ticket_id: str):
    """Eliminar un ticket por su ID"""
    ticket = Ticket.objects.get(ticket_id=ticket_id)
    ticket.delete()
    return {"message": "Ticket eliminado correctamente"}