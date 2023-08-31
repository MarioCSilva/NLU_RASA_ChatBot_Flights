# generic imports
from ast import Constant
import configparser
import logging
import aux.constants as Constants
import os
import inspect

# Logger
logging.basicConfig(
    format="%(module)-15s:%(levelname)-10s| %(message)s",
    level=logging.INFO
)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

def load_config():
    # load config
    config = configparser.ConfigParser()
    config.read('config.ini')
    try:
        Constants.DB_LOCATION = config['DB']['Location']
        Constants.DB_NAME = config['DB']['Name']
        Constants.DB_USER = config['DB']['User']
        Constants.DB_PASSWORD = config['DB']['Password']
        Constants.ACCESS_KEY = config['EXTERNAL_API']['AccessKey']
        Constants.AVIATIONSTACK_HOST = config['EXTERNAL_API']['Host']
        Constants.CHATBOT_HOST = config['CHATBOT']['Host']

    except Exception as e:
        return False, "Make sure to define the required variables on the config file"
    return True, "Database Connected.."
