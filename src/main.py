import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from src.init import redis_connector
from src.api.hotels import router as hotels_router
from src.api.auth import router as auth_router
from src.api.bookings import router as bookings_router
from src.api.facilities import router as facilities_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_connector.connect()
    yield
    await redis_connector.close()
app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(bookings_router)
app.include_router(facilities_router)

if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
