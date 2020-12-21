from fastapi import FastAPI

from backend.handlers import managers_route


app = FastAPI()

app.include_router(managers_route)
