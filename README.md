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
