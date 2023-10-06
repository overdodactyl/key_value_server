# Key-Value Store Server

## Overview

This project is a simple key-value store server built using Flask, designed to handle basic CRUD (Create, Read, Update, Delete) operations on key-value pairs. It provides an HTTP API that allows clients to interact with the server.

Pers

## Files

- `key_value_server.py`: The main Flask application file that defines the server routes and operations.
- `tests.py`: Contains a set of test cases to verify the functionality of the server.

## Requirements

This project was written using Python 3.9.17.  See `requirements.txt` for a list of dependencies.


You can install these dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

To start the server, run the following command:

```bash
python key_value_server.py
```

The server will be running on port 8080 on localhost by default.  You can change this by setting the `PORT` and `HOST` variables.

## Running Tests

To run the test suite, run the following command:

```bash
python tests.py
```

## Notes

This project includes data persistence using a JSON file (defined by `PERSISTENCE_INTERVAL_SECONDS`, `DATA_DIRECTORY`, and `DATA_FILE_PATH`) to store the key-value pairs. The server periodically saves the data to the file, ensuring that data is retained even if the server is restarted.

## Dockerization

This project includes a Dockerfile that can be used to build a Docker image for the server.  To build the image, run the following command:

```bash
docker build -t key-value-server .
```

To run the server in a Docker container, run the following command:

```bash
docker run -p 8080:8080 key-value-server
```

### Sample Requests

Once the server is running, you can interact with it using the following sample requests:

#### Create a key-value pair

```bash
curl -X POST -H "Content-Type: application/json" -d '{"key": "new_key", "value": "new_value"}' http://localhost:8080/put

```
#### Read a key-value pair

```bash
curl http://localhost:8080/get?key=new_key
```

In order to stop and remove the container, run the following commands:

```bash
docker stop <container_id>
docker rm <container_id>
```