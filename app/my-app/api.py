import requests

# define the request payload
payload = {
    'message': 'Hello from Python!'
}

# send the POST request
response = requests.post('http://192.168.137.213:3000/api/messages', json=payload)

# print the response from the server
print(response.json())