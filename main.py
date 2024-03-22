# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс User с полями id, name, email и password.
# Создайте список users для хранения пользователей.
# Создайте маршрут для отображения списка пользователей (метод GET).
# Реализуйте вывод списка пользователей через шаблонизатор Jinja.


from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
import uvicorn
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    id_: int
    name: str
    email: Optional[str] = None
    password: str


users = []

for i in range(1, 10):
    user = User(id_=i, name=f"name_{i}", email=f"name_{i}@gmail.com", password=str(i)*6)
    users.append(user)


@app.get('/root/')
async def root():
    return users


@app.get("/", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "users": users})


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8001)