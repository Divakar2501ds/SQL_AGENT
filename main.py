from fastapi import FastAPI
from router.chatbot import router

app = FastAPI()

app.include_router(router=router)