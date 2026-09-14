import os
from mongoengine import connect

def connect_mongo():
    connect(
     db=os.getenv('MONGO_DB', 'ticketera'),
     host=os.getenv('MONGO_HOST', 'localhost'),
     port=int(os.getenv('MONGO_PORT', '27017')),
    )