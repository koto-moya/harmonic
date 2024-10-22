import requests
from config import server_endpoint

# need requests for gestalts harmonic endpoints 

# basically I am doing RDD for api's

class Token:
    token: str = None

def gestalt_get(token, endpoint, payload=None):
    headers = {"Authorization":f"Bearer {token}",
               "Content-Type": "application/json"}
    response = requests.get(server_endpoint+endpoint, headers=headers, params=payload)
    if response.status_code == 200:
        items = response.json()
        return items


def gestalt_post(token, endpoint, payload=None):
    headers = {"Authorization":f"Bearer {token}",
               "Content-Type": "application/json"}
    requests.post(server_endpoint+endpoint, headers=headers, json=payload)

def login(username, password):
    data = {"username":username,
            "password":password}
    try:
        response = requests.post(server_endpoint+"/token", data=data)
        if response.status_code == 200:
            token = Token()
            token_data = response.json()
            token.token = token_data.get("access_token")
        return token.token
    except:
        return  