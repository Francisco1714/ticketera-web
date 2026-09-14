import os
from fastapi import FastAPI
from mongoengine import connect

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