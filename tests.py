import requests

key = "myKey"
value = "myValue3"
server_url = "http://127.0.0.1:8080"
# server_url= "http://localhost"

# For PUT operation, FastAPI expects the 'key' as a query parameter and 'value' in the JSON body
put_response = requests.post(f'{server_url}/put', params={'key': key}, json={'value': value})
print("PUT Response Status Code:", put_response.status_code)  # Check if the request was successful

# For GET operation, FastAPI now also expects the 'key' as a query parameter
get_response = requests.get(f'{server_url}/get', params={'key': key})
print("GET Response Status Code:", get_response.status_code)  # Check if the request was successful
if get_response.status_code == 200:
    print("GET Response JSON:", get_response.json())  # Get the JSON response content

# For DELETE operation, FastAPI now also expects the 'key' as a query parameter
delete_response = requests.delete(f'{server_url}/del', params={'key': key})
print("DELETE Response Status Code:", delete_response.status_code)  # Check if the request was successful
