import requests
import time
import random
import string
import json

HAPROXY_URL = "http://localhost"


def send_put_request(key, value):
    # Construct the payload
    payload = json.dumps({"value": value})
    headers = {'Content-Type': 'application/json'}
    # Construct the URL with the key as a URL parameter
    URL = f"{HAPROXY_URL}/put?key={key}"

    # Send the request to HAProxy
    response = requests.post(URL, headers=headers, data=payload)

    # Return the response text (ideally, this should include the instance ID)
    return response.json()


def send_get_request(key):
    response = requests.get(f"{HAPROXY_URL}/get?key={key}")
    return response.json()


def generate_random_string(length=10):
    # Generate a random string of fixed length
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


instance_count = {'KVStore1': 0, 'KVStore2': 0, 'KVStore3': 0}

retrieve_errors = 0

for i in range(100):
    key = generate_random_string()
    value = generate_random_string()

    # Send PUT request
    put_response = send_put_request(key, value)
    put_instance_id = put_response.get('instance', 'Unknown')  # Fallback to 'Unknown' if not found
    instance_count[put_instance_id] = instance_count.get(put_instance_id, 0) + 1

    # Sleep briefly to allow for replication if necessary (depending on how your KV store works)
    time.sleep(0.1)

    # Send GET request
    get_response = send_get_request(key)

    # Verify that the GET request retrieves the correct data
    if get_response.get('status') == 'success' and value in get_response.get('value', []):
        # print(f"Success! Retrieved key '{key}' with value '{value}'.")
        pass
    else:
        retrieve_errors += 1
        # print(f"Error! Key '{key}' was not retrieved successfully. Response: {get_response}")

# Print the count of responses per instancetest
for instance, count in instance_count.items():
    print(f"{instance} received {count} requests.")

print(f"Number of retrieval errors: {retrieve_errors}")
