import configparser

def get_api_key():
    config = configparser.ConfigParser()
    config.read("config.ini")
    if 'API' in config and 'api_key' in config['API']:
        return config['API']['api_key']
    return ''

def save_api_key():
    config = configparser.ConfigParser()
    config.read("config.ini")
    config.set("API", "key", self.api_key_entry.get())
    with open("config.ini", "w") as configfile:
        config.write(configfile)

def save_api_key_to_file():
    self.save_api_key()
    self.status_label.config(text="API Key saved.")
