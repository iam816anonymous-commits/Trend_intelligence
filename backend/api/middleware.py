from fastapi import Request
import time
import logging

logger = logging.getLogger("api")

async def log_requests_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Method: {request.method} Path: {request.url.path} Duration: {process_time:.4f}s Status: {response.status_code}")
    response.headers["X-Process-Time"] = str(process_time)
    return response
