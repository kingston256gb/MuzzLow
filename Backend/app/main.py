import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.playlist import router as playlist_router
from app.routers.search import router as search_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(playlist_router)
app.include_router(search_router)

@app.get("/")
async def root():
    return {
        "msg": "Welcome to the MuzzLow WEB Backend!",
        "ok": True
    }

if __name__ == "__main__":
    uvicorn.run('main:app' , port=8000, reload=True)