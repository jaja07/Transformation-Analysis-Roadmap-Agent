from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application démarrée. Les migrations sont gérées par Alembic.")
    yield
    print("Fermeture de l'application...")

app = FastAPI(
    title="TARA - Transformation Analysis & Roadmap Agent",
    description="API pour le système multi-agents de génération de roadmap",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/", tags=["Health"])
async def root():
    return {"message": "API is running", "status": "ok"}


def main():
    """Point d'entrée pour lancer l'application localement via Uvicorn."""
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
