# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс User с полями id, name, email и password.
# Создайте список users для хранения пользователей.
# Создайте маршрут для отображения списка пользователей (метод GET, POST, PUT, DELETE).
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

@app.post('/user/')
async def creat_user(user: User):
    users.append(user)
    return user


@app.put('/user/{id_}')
async def update_user(id_: int, user: User):
    for i in range(len(users)):
        if users[i].id_ == id_:
            users[i] = user
    return {'id_': id_, 'user': user}


@app.delete('/user/{id_}')
async def delete_user(id_: int):
    for us in users:
        if us.id_ == id_:
            users.remove(us)
    return {'id_': id_}


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8001)
