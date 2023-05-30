import os, json, time, api

def get_base_path():
    return os.path.abspath(".")

def resource_path(relative_path):
    base_path = get_base_path() # or sys._MEIPASS
    return os.path.join(base_path, relative_path)

def create_config():
    if os.path.exists(resource_path("config.json")):
        return False

    with open(resource_path("config.json"), "w") as file:
        json.dump({
            "key": "",
            "delay": 25
        }, file, indent=2)
        file.close()
        return True
    
def get_config():
    with open(resource_path("config.json")) as file:
        data = json.load(file)
        file.close()
        return data
    
def update_config(config_data):
    with open(resource_path("config.json"), "w") as file:
        json.dump(config_data, file, indent=2)
        file.close()
        return True

def create_white_list():
    if os.path.exists(resource_path("whitelist.json")):
        return False

    with open(resource_path("whitelist.json"), "w") as file:
        json.dump([
            "",
        ], file, indent=2)
        file.close()
        return True

def get_white_list():
    with open(resource_path("whitelist.json")) as file:
        data = json.load(file)
        file.close()
        return data

def is_white_listed(token: str):
    return token in get_white_list()

def confirm(text: str):
    return input(f"{text}: ") in ["y", "Y", "yes", "ye", "1"]

def main_thread():
    config = get_config()

    if not config["key"]:
        key = input("Mullvad VPN: ")

        if confirm("Save this key? (y/N)"):
            config["key"] = key
            update_config(config)
            config = get_config()

    auth_token = api.get_auth_token(config["key"])

    while True:
        device_list = api.get_device_list(auth_token)

        for device in device_list:
            pub_key = api.get_device_public_key(device)

            if is_white_listed(pub_key):
                continue

            api.device_kick(auth_token, pub_key)

        print(f"Devices: {len(device_list)}")

        time.sleep(20) # Delay

if __name__ == "__main__":
    create_config()
    create_white_list()
    main_thread()