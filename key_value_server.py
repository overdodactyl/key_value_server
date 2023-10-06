from flask import Flask, request, jsonify
import logging
import threading
import time
import json
import os

# Global constants
DATA_DIRECTORY = "data"
DATA_FILE_PATH = "key_value_data.json"
LOG_FILE_PATH = "logs/server_logs.log"
PERSISTENCE_INTERVAL_SECONDS = 10
DATA_FILE_PATH = os.path.join(DATA_DIRECTORY, "key_value_data.json")

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

    # Create a file handler and set the log file path
    file_handler = logging.FileHandler(log_file_path)

    # Create a formatter for the log messages
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)


def initialize_kv_store(data_file_path):
    """
    Function to initialize the key-value store
        If the data file exists, load the data from the file
        Otherwise, initialize an empty dictionary
    :param data_file_path: Path to the data file
    :return: The key-value store
    """
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

# Initialize the key-value store
kv_store = initialize_kv_store(DATA_FILE_PATH)

# Create a lock for thread safety
# This lock will be used to synchronize access to the key-value store
kv_store_lock = threading.Lock()


# Define a route for PUT requests
@app.route("/put", methods=["POST"])
def put():
    """
    Function to handle PUT requests
    PUT requests are used to add a new key-value pair to the key-value store
    If the key already exists, the new value is appended to the list of values for the key
    :return: A response indicating success or failure
    """
    # Get the key and value from the request body
    data = request.get_json()
    key = data.get("key")
    value = data.get("value")

    # Check if the key or value is missing
    # If so, return an error response
    if key is None or value is None:
        logger.error("Invalid PUT request: Missing key or value")
        return jsonify({"status": "error", "message": "Invalid request"}), 400

    # Acquire the lock before modifying the dictionary
    # This ensures that only one thread is modifying the dictionary at a time
    with kv_store_lock:
        if key in kv_store:
            if isinstance(kv_store[key], list):
                kv_store[key].append(value)
            else:
                kv_store[key] = [kv_store[key], value]
        else:
            kv_store[key] = [value]

    # Log the PUT operation
    logger.info(f"PUT operation - Key: {key}, Value: {value}")

    return jsonify({"status": "success"})


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
        logger.info(f"GET operation - Key: {key}, Value: {kv_store[key]}")
        return jsonify({"status": "success", "value": kv_store[key]})
    else:
        # Log the error
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
        logger.info(f"DEL operation - Key: {key}")

        return jsonify({"status": "success"})
    else:
        logger.error(f"DEL operation - Key not found: {key}")
        return jsonify({"status": "error", "message": "Key not found"}), 404


if __name__ == "__main__":
    start_save_thread()
    app.run(host="localhost", port=8080)
