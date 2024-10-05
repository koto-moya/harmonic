import requests
from config import server_endpoint

# need requests for gestalts harmonic endpoints 

# basically I am doing RDD for api's

class Token:
    token: str = None


def get_combo_boxes(token, endpoint):
    headers = {"":f"Bearer {token}",
               "Content-Type": {"application/json"}}
    try:
        response = requests.get(server_endpoint+endpoint, headers=headers)
        if response.status_code == 200:
            items = response.json()
            return items
    except:
        return ["test"]
    
    

def login(useraname, password):
    return Token()

# def login(username, password):
#     data = {
#         "username": username,
#         "password": password
#     }
#     try:
#         response = requests.post(server_endpoint+"/token", data=data)
#         if response.status_code == 200:
#             token_data = response.json()
#             access_token = token_data.get("access_token")
#             return access_token
#     except:
#         return None