# Key-Value Store Server

## Overview

This project is a simple key-value store server built using Flask, designed to handle basic CRUD (Create, Read, Update, Delete) operations on key-value pairs. It provides an HTTP API that allows clients to interact with the server.

Additionally, it includes a set of test cases to verify the functionality of the server as well as the necessary infrastructure to run mulitple instances of the server in parallel using Docker and consistant hashing.

## Files

- `key_value_server.py`: The main FastAPI application file that defines the server routes and operations.
- `tests.py`: Contains a few test cases to verify the functionality of the server and show sample usage.
- `Dockerfile`: Defines the Docker image for the server.
- `requirements.txt`: Contains a list of dependencies for the project.
- `requirements_kv_server.txt`: Contains a list of dependencies for the server only.
- `haproxy.cfg`: Defines the HAProxy configuration for the load balancer.
- `shell/build.sh`: Builds the Docker image for the server and posts it to DockerHub.
- `shell/benchmark.sh`: Runs a benchmark test on the server.

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

## Multiple Instances and Benchmarking

To run multiple instances of the server in parallel, you can use Docker and HAProxy.

The key-value server has been posted to DockerHub.  The `shell/benchmark.sh` script launches HAProxy, the three servers, and runs the benchmarking code. 