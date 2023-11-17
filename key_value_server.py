from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import logging
import ujson as json
import os
import asyncio

# Global constants
DATA_DIRECTORY = "data"
DATA_FILE_PATH = os.path.join(DATA_DIRECTORY, "key_value_data.json")
LOG_FILE_PATH = "logs/server_logs.log"
PERSISTENCE_INTERVAL_SECONDS = 600
PORT = int(os.environ.get("KV_STORE_PORT", 8080))
HOST = "localhost"


# Setup logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE_PATH), logging.StreamHandler()]
)

logger = logging.getLogger("key_value_server")


try:
    with open(DATA_FILE_PATH, "r") as data_file:
        kv_store = json.load(data_file)
except FileNotFoundError:
    kv_store = {}

class Item(BaseModel):
    value: str


app = FastAPI()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(save_data_to_disk())

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

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(save_data_to_disk())

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Server is shutting down. Saving data...")
    await save_data_now()  # Function to save data immediately

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
    uvicorn.run(app, host=HOST, port=PORT)
