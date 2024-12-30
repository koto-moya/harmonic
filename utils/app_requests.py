import requests
from config import server_endpoint
from pydantic import BaseModel

class ConfigParams(BaseModel):
    config_name: str
    batch: bool

    class Config:
        extra = 'allow'

class Token:
    token: str = None

    
def gestalt_get(token: str, payload):
    headers = {"Authorization":f"Bearer {token}",
               "Content-Type": "application/json"}
    response = requests.get(server_endpoint+"/get", headers=headers, params=payload)
    if response.status_code == 200:
        response = response.json()
        print(response[0],"\n", response[1])
        return response[0], response[1] # x, y

def gestalt_post(token: str, payload: ConfigParams):
    headers = {"Authorization":f"Bearer {token}",
               "Content-Type": "application/json"}
    response = requests.post(server_endpoint+"/post", headers=headers, json=payload)
    return response.text

def gestalt_post_stream(token, endpoint, payload=None):
    headers = {"Authorization":f"Bearer {token}",
               "Content-Type": "application/json"}
    with requests.post(server_endpoint+endpoint, headers=headers, json=payload, stream=True) as response:
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=1, decode_unicode=True):
            yield chunk

def login(username: str, password: str) -> str:
    data = {"username":username,
            "password":password}
    try:
        response = requests.post(server_endpoint+"/token", data=data)
        if response.status_code == 200:
            token = Token()
            token_data = response.json()
            token.token = token_data.get("access_token")
        return token
    except:
        return None 