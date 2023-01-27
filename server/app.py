from flask import Flask, jsonify
from config import ui_config, server_config
from lib import flirc_utils

app = Flask(__name__)

@app.route("/ui")
def ui():
 return jsonify(ui_config)

@app.route("/cmd/<requested_command>")
def cmd(requested_command):
 for command in server_config["commands"]:
  if command["name"] == requested_command:
   flirc_utils.send_ir(server_config["flirc"]["flirc_util_path"], server_config["flirc"]["flirc_util_binary_name"], server_config["flirc"]["additional_arguments"], command["patterns"])
   return jsonify({"result": "done"})
 return jsonify({"result": f"Error: unknown command {requested_command}"})