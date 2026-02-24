""" Main module for API"""
from fastapi import FastAPI
from routers import health
from routers import crud

app = FastAPI(
    title = "Shoppi API", version = "0.1"
)

app.include_router(health.router)
app.include_router(crud.router)
