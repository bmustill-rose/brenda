import sys
import os
import requests
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from config import ui_config, server_config

def get_ui_config():
 if "remote_config_url" in ui_config:
  return requests.get(ui_config["remote_config_url"]).json()["ui_config"]
 else:
  return ui_config

def get_server_config():
 if "remote_config_url" in server_config:
  return requests.get(server_config["remote_config_url"]).json()["server_config"]
 else:
  return server_config