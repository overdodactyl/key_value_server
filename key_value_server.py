from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import ujson as json
import os
import asyncio
from fastapi.responses import ORJSONResponse
from fastapi.middleware.gzip import GZipMiddleware

# Global constants
DATA_DIRECTORY = "data"
DATA_FILE_PATH = os.path.join(DATA_DIRECTORY, "key_value_data.json")
LOG_FILE_PATH = "logs/server_logs.log"
PERSISTENCE_INTERVAL_SECONDS = 600
PORT = int(os.environ.get("KV_STORE_PORT", 8080))
HOST = "localhost"

# Setup logger
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE_PATH), logging.StreamHandler()]
)

logger = logging.getLogger("key_value_server")

# Load initial data
try:
    with open(DATA_FILE_PATH, "r") as data_file:
        kv_store = json.load(data_file)
except FileNotFoundError:
    kv_store = {}

# Response models
class Item(BaseModel):
    value: str

class KeyValueResponse(BaseModel):
    status: str
    value: str = None

class SuccessResponse(BaseModel):
    status: str

# FastAPI app with ORJSONResponse for faster JSON handling and GZipMiddleware for compression
app = FastAPI(default_response_class=ORJSONResponse)
app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.post("/put", response_model=SuccessResponse)
async def put(key: str, item: Item):
    if key is None or item.value is None:
        logger.error("Invalid PUT request: Missing key or value")
        raise HTTPException(status_code=400, detail="Invalid request")

    kv_store[key] = item.value
    return {"status": "success"}

@app.get("/get", response_model=KeyValueResponse)
async def get(key: str):
    if key not in kv_store:
        logger.error(f"GET operation - Key not found: {key}")
        raise HTTPException(status_code=404, detail="Key not found")

    return {"status": "success", "value": kv_store[key]}

@app.delete("/del", response_model=SuccessResponse)
async def delete(key: str):
    if key not in kv_store:
        logger.error(f"DEL operation - Key not found: {key}")
        raise HTTPException(status_code=404, detail="Key not found")

    del kv_store[key]
    return {"status": "success"}


# Lifespan event handlers
async def on_startup():
    # Your startup logic here
    asyncio.create_task(save_data_to_disk())

async def on_shutdown():
    # Your shutdown logic here
    logger.info("Server is shutting down. Saving data...")
    await save_data_now()

app.router.add_event_handler("startup", on_startup)
app.router.add_event_handler("shutdown", on_shutdown)


async def save_data_now():
    try:
        with open(DATA_FILE_PATH, "w") as data_file:
            json.dump(kv_store, data_file)
    except Exception as e:
        logger.error(f"Error saving data: {e}")

async def save_data_to_disk():
    while True:
        await save_data_now()
        await asyncio.sleep(PERSISTENCE_INTERVAL_SECONDS)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT, http="h11", loop="asyncio", log_level="warning")
