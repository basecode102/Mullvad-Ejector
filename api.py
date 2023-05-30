import requests

api_addr = "https://api-www.mullvad.net/www/"

def get_auth_token(key: str):
    response = requests.get(api_addr + f"accounts/{key}/")

    if response.status_code != 200:
        print(response)
        return False

    response = response.json()

    try:
        if response["code"]:
            print(response["code"])
            return False
    except:
        return response["auth_token"]

def get_account_data(auth_token: str):
    headers = {
        "Authorization": f"Token {auth_token}"
    }

    response = requests.get(api_addr + f"me/", headers=headers)

    if response.status_code != 200:
        print(response)
        return False
    
    response = response.json()

    try:
        if response["code"]:
            print(response["code"])
            return False
    except:
        pass

    return response

def get_device_list(auth_token):
    headers = {
        "Authorization": f"Token {auth_token}"
    }

    response = requests.get(api_addr + f"me/", headers=headers)

    if response.status_code != 200:
        print(response)
        return False
    
    response = response.json()

    try:
        if response["code"]:
            print(response["code"])
            return False
    except:
        pass
    
    response = response["account"]["wg_peers"]

    return response

def get_device_public_key(device):
    return device["key"]["public"]

def device_kick(auth_token: str, pub_key: str):
    headers = {
        "Authorization": f"Token {auth_token}",
        "Content-type": "application/json", 
        "Accept": "application/json"

    }

    response = requests.post(api_addr + f"wg-pubkeys/revoke/", json={
        "pubkey": pub_key
    }, headers=headers)

    if response.status_code not in [200, 204]:
        print(response)
        return False

    try:
        response = response.json()

        if response["code"]:
            print(response["code"])
            return False
    except:
        pass

    return True