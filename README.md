# Key-Value Store Server

## Overview

This project is a simple key-value store server built using Flask, designed to handle basic CRUD (Create, Read, Update, Delete) operations on key-value pairs. It provides an HTTP API that allows clients to interact with the server.

Additionally, it includes a set of test cases to verify the functionality of the server as well as the necessary infrastructure to run mulitple instances of the server in parallel using Docker and consistant hashing.

## Files

- `key_value_server.py`: The main Flask application file that defines the server routes and operations.
- `tests.py`: Contains a set of test cases to verify the functionality of the server.
- `Dockerfile`: Defines the Docker image for the server.
- `requirements.txt`: Contains a list of dependencies for the project.
-  `haproxy.cfg`: Defines the HAProxy configuration for the load balancer.
- `locustfile.py`: Contains a set of load tests for the server.
- `locust_results.py`: Contains a set of functions to process the results of the load tests.
- `performance.sh`: A bash script that runs the load tests and processes the results.

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
docker build -t key-value-store .
```

## HAProxy

The HAProxy load balancer is configured to run on port 80.  To start the load balancer, run the following command:

```bash
 docker run -d -v $(pwd)/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro -p 80:80 -p 8404:8404 haproxy:latest
```

The default configuration is set to work with up to 3 instances. 


