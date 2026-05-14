from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/analyze")
async def analyze(payload: dict):
    return {"result": "analysis placeholder", "input": payload}
