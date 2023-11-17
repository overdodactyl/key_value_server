from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import json
import os
import asyncio

# Global constants
DATA_DIRECTORY = "data"
DATA_FILE_PATH = os.path.join(DATA_DIRECTORY, "key_value_data.json")
LOG_FILE_PATH = "logs/server_logs.log"
PERSISTENCE_INTERVAL_SECONDS = 60
PORT = int(os.environ.get("KV_STORE_PORT", 8080))
HOST = "localhost"

# Create data directory if it doesn't exist
os.makedirs(DATA_DIRECTORY, exist_ok=True)

# Setup logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE_PATH), logging.StreamHandler()]
)

logger = logging.getLogger("key_value_server")
kv_store = {}

# Initialize the key-value store
try:
    with open(DATA_FILE_PATH, "r") as data_file:
        kv_store = json.load(data_file)
except FileNotFoundError:
    kv_store = {}


class Item(BaseModel):
    value: str


app = FastAPI()


@app.post("/put")
async def put(key: str, item: Item):
    if key is None or item.value is None:
        logger.error("Invalid PUT request: Missing key or value")
        raise HTTPException(status_code=400, detail="Invalid request")

    kv_store[key] = item.value
    return {"status": "success"}


@app.get("/get")
async def get(key: str):
    if key not in kv_store:
        logger.error(f"GET operation - Key not found: {key}")
        raise HTTPException(status_code=404, detail="Key not found")

    return {"value": kv_store[key]}


@app.delete("/del")
async def delete(key: str):
    if key not in kv_store:
        logger.error(f"DEL operation - Key not found: {key}")
        raise HTTPException(status_code=404, detail="Key not found")

    del kv_store[key]
    return {"status": "success"}

@app.get('/health')
async def health_check():
    return "OK"


async def save_data_to_disk():
    while True:
        with open(DATA_FILE_PATH, "w") as data_file:
            json.dump(kv_store, data_file)
        await asyncio.sleep(PERSISTENCE_INTERVAL_SECONDS)


if __name__ == "__main__":
    # Run the periodic data saving in the background
    # asyncio.create_task(save_data_to_disk())

    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
