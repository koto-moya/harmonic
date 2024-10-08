import requests
from config import server_endpoint

# need requests for gestalts harmonic endpoints 

# basically I am doing RDD for api's

class Token:
    token: str = None

def get_combo_boxes(token, endpoint):
    headers = {"Authorization":f"Bearer {token}",
               "Content-Type": "application/json"}
    response = requests.get(server_endpoint+endpoint, headers=headers)
    if response.status_code == 200:
        items = response.json()
        return items
    
def get_performance(token, payload):
    headers = {"Authorization":f"Bearer {token}",
               "Content-Type": "application/json"}
    response = requests.get(server_endpoint+"/getperformance", headers=headers, params=payload)
    if response.status_code == 200:
        data = response.json()
        return data

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