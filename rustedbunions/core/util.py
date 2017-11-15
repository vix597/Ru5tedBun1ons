from uuid import uuid4

def ObjectId():
    return str(uuid4()).replace('-', '')
