from flask import Flask, request, jsonify
import logging
# import threading
import time
import json
import os

# Global constants
DATA_DIRECTORY = "data"
DATA_FILE_PATH = "key_value_data.json"
LOG_FILE_PATH = "logs/server_logs.log"
PERSISTENCE_INTERVAL_SECONDS = 60
DATA_FILE_PATH = os.path.join(DATA_DIRECTORY, "key_value_data.json")
PORT = int(os.environ.get("KV_STORE_PORT", 8080))
HOST = "localhost"

# Create data directory if it doesn't exist
os.makedirs(DATA_DIRECTORY, exist_ok=True)

def setup_logger(logger, log_file_path):
    """
    Function to setup the logger
    :param logger: The logger object
    :param log_file_path: Path to the log file
    :return:
    """
    logger.setLevel(logging.INFO)

    # Create directory for log file if it does not exist
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # Create a file handler and set the log file path
    file_handler = logging.FileHandler(log_file_path)

    # Create a formatter for the log messages
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)


def initialize_kv_store(data_file_path, init = False):
    """
    Function to initialize the key-value store
        If the data file exists, load the data from the file
        Otherwise, initialize an empty dictionary
    :param data_file_path: Path to the data file
    :return: The key-value store
    """

    if init:
        kv_store = {}
    else:
        try:
            with open(data_file_path, "r") as data_file:
                kv_store = json.load(data_file)
        except FileNotFoundError:
            kv_store = {}

    return kv_store


def start_save_thread():
    """
    Function to start a separate thread for data-saving
    :return:
    """
    save_thread = threading.Thread(target=save_data_to_disk)
    save_thread.daemon = True
    save_thread.start()


def save_data_to_disk(interval_seconds=PERSISTENCE_INTERVAL_SECONDS):
    """
    Function to periodically save data to disk
        This creates persistent storage for the key-value store
    :param interval_seconds: Interval between successive saves
    :return: None
    """

    while True:
        # Save the key-value store data to the file
        with open(DATA_FILE_PATH, "w") as data_file:
            json.dump(kv_store, data_file)

        # Sleep for the specified interval before saving again
        time.sleep(interval_seconds)


app = Flask(__name__)

# Initialize a logger
logger = logging.getLogger("key_value_server")
setup_logger(logger, LOG_FILE_PATH)

logger.info("Initialized Logger")

# Initialize the key-value store
kv_store = initialize_kv_store(DATA_FILE_PATH, init=True)

# Create a lock for thread safety
# This lock will be used to synchronize access to the key-value store
kv_store_lock = threading.Lock()


# Define a route for PUT requests
@app.route("/put", methods=["POST"])
def put():
    """
    Function to handle PUT requests.
    PUT requests are used to add or update a key-value pair in the key-value store.
    If the key already exists, the value is replaced with the new value.
    :return: A response indicating success or failure.
    """
    # Get the key and value from the request body
    data = request.get_json()
    key = request.args.get("key")
    value = data.get("value")

    # Check if the key or value is missing
    # If so, return an error response
    if key is None or value is None:
        logger.error("Invalid PUT request: Missing key or value")
        return jsonify({"message": "Invalid request"}), 400

    # Acquire the lock before modifying the dictionary
    # This ensures that only one thread is modifying the dictionary at a time
    with kv_store_lock:
        kv_store[key] = value

    # Log the PUT operation
    # logger.info(f"PUT operation - Key: {key}, Value: {value}")

    return '', 200


# Define a route for GET requests
@app.route("/get")
def get():
    """
    Function to handle GET requests
    GET requests are used to retrieve the value for a given key
    If the key has multiple values, all values are returned
    :return: A response containing the value(s) for the given key
    """
    # Get the key from the request arguments
    key = request.args.get("key")
    if key in kv_store:
        # Log the GET operation
        # logger.info(f"GET operation - Key: {key}, Value: {kv_store[key]}")
        return jsonify({"value": kv_store[key]}), 200
    else:
        logger.error(f"GET operation - Key not found: {key}")
        return jsonify({"status": "error", "message": "Key not found"}), 404


# Define a route for DEL requests
@app.route("/del", methods=["DELETE"])
def delete():
    """
    Function to handle DEL requests
    DEL requests are used to delete a key from the key-value store
    :param key: The key to delete
    :return: A response indicating success or failure
    """
    key = request.args.get("key")
    if key in kv_store:
        # Acquire the lock before modifying the dictionary
        with kv_store_lock:
            del kv_store[key]
        # Log the DEL operation
        # logger.info(f"DEL operation - Key: {key}")

        return jsonify({"status": "success"})
    else:
        logger.error(f"DEL operation - Key not found: {key}")
        return jsonify({"status": "error", "message": "Key not found"}), 404


@app.route('/health', methods=['GET'])
def health_check():
    return "OK", 200

if __name__ == "__main__":
    # start_save_thread()
    app.run(host="0.0.0.0", port=8080)
