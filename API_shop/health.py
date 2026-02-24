""" Health status module """
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter(tags=["Server Status"])

@router.get("/")
def main():
    """ Main endpoint. Redirect to server status"""
    return RedirectResponse("/health")

@router.get("/health")
def server_status():
    """ Verify server status """
    return {"status": "server is up and running"}
