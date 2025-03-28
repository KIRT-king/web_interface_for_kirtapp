import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router_auth import router as router_auth
from router_crud import router as router_crud
app = FastAPI()

app.include_router(router_auth, prefix = "/auth", tags = ["auth"])
app.include_router(router_crud, prefix = "/crud", tags = ["crud"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],  # Разрешаем запросы с фронта (или "*", если разрешаем всем)
    allow_credentials=True,  # Разрешаем куки
    allow_methods=["*"],  # Разрешаем все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8002)