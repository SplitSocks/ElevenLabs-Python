# name api_utils.py
import configparser

def set_api_key(new_api_key):
    # create a ConfigParser object and read the INI file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # set the new API key in the ConfigParser object
    config.set('API_KEYS', 'ElevenLABS', new_api_key)

    # write the changes back to the INI file
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    
def get_api_key():
    # create a ConfigParser object and read the INI file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # get the value of the "ElevenLABS" key under the "API_KEYS" section
    api_key = config.get('API_KEYS', 'ElevenLABS')

    # check if the API key is empty
    if not api_key:
        return "No API KEY"
    
    return api_key