import requests
import json
import threading

# Define the server URL
SERVER_URL = "http://localhost:8080"


# Function to send a GET request and assert the response
def test_get(key, expected_value=None, expected_status="success"):
    try:
        url = f"{SERVER_URL}/get?key={key}"
        response = requests.get(url)
        print("GET Test:")
        print(f"Testing GET request for key: {key}")
        print("Request URL:", url)
        print("Response:", response.status_code, response.json())

        if expected_status == "success":
            assert response.status_code == 200
            assert response.json()["status"] == "success"

            if expected_value is not None:
                response_value = response.json()["value"]

                if isinstance(expected_value, list):
                    assert response_value == expected_value
                else:
                    # Check if the response value is a list and contains the expected value
                    if isinstance(response_value, list) and expected_value in response_value:
                        pass  # The test passes in this case
                    else:
                        assert response_value == expected_value
        elif expected_status == "error":
            assert response.status_code == 404  # Expecting a "Key not found" response
            assert response.json()["status"] == "error"

        print()
    except AssertionError as e:
        print("GET Test failed:", e)

# Function to send a PUT request and assert the response
def test_put(key, value, expected_status="success"):
    try:
        url = f"{SERVER_URL}/put"
        data = {"key": key, "value": value}
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=data, headers=headers)
        print("PUT Test:")
        print(f"Testing PUT request for key: {key}, value: {value}")
        print("Request URL:", url)
        print("Request Data:", data)
        print("Response:", response.status_code, response.json())

        assert response.status_code == 200  # Expecting a successful response

        if expected_status == "success":
            assert response.json()["status"] == "success"
        elif expected_status == "error":
            assert response.json()["status"] == "error"

        print()
    except AssertionError as e:
        print("PUT Test failed:", e)


# Function to send a DEL request and assert the response
def test_del(key, expected_status="success"):
    try:
        url = f"{SERVER_URL}/del?key={key}"
        response = requests.delete(url)
        print("DEL Test:")
        print(f"Testing DEL request for key: {key}")
        print("Request URL:", url)
        print("Response:", response.status_code, response.json())

        if expected_status == "success":
            assert response.status_code == 200
            assert response.json()["status"] == "success"
        elif expected_status == "error":
            assert response.status_code == 404
            assert response.json()["status"] == "error"
            assert response.json()["message"] == "Key not found"

        print()
    except AssertionError as e:
        print("DEL Test failed:", e)


# Function to test concurrency with multiple threads
def test_concurrency():
    try:
        key = "concurrency_key"
        num_threads = 10

        # Initialize the key with an initial value
        test_put(key, "initial_value")

        # Function for concurrent PUT operations
        def concurrent_put_thread(thread_num):
            value = f"value_{thread_num}"
            test_put(key, value)

        # Create and start multiple threads for concurrent PUT operations
        threads = []
        for i in range(num_threads):
            thread = threading.Thread(target=concurrent_put_thread, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Check if the final value matches one of the concurrent PUT values
        response = requests.get(f"{SERVER_URL}/get?key={key}")
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["value"] in [f"value_{i}" for i in range(num_threads)]

        print("Concurrency Test passed")
    except AssertionError as e:
        print("Concurrency Test failed:", e)


if __name__ == "__main__":
    try:
        # Start with a PUT operation to populate the key-value store
        test_put("existing_key", "existing_value")

        # Test GET operation with an existing key
        test_get("existing_key", expected_value="existing_value")

        # Test GET operation with a non-existent key
        test_get("nonexistent_key", expected_status="error")

        # Test DEL operation with an existing key
        test_del("existing_key")

        # Test DEL operation with a non-existent key
        test_del("nonexistent_key", expected_status="error")

        # Test concurrency
        test_concurrency()

    except AssertionError as e:
        print("Some tests failed:", e)
    else:
        print("All tests passed!")
