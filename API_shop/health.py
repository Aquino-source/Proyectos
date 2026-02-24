""" Health status module """
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def server_status():
    """ Verify server status """
    return {"status": "server is up and running"}
