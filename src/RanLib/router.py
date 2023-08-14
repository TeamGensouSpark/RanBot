import nonebot
from fastapi import FastAPI

app: FastAPI = nonebot.get_app()

def registerGet():
    return app.get()
