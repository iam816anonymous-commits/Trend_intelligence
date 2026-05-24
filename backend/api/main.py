from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .config import settings
from .router import router as api_router
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")

app = FastAPI(title="TrendPulse AI API")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred.", "detail": str(exc)},
    )

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to TrendPulse AI India"}
