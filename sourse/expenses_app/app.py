from fastapi import FastAPI

from .routers import router


app = FastAPI(
    title='Expenses app',
    description='Приложение учета личного бюджета',
    version='1.0.0'
)

app.include_router(router)











