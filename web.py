import os
from flask import Flask, jsonify
import ConfigParser

from ARKDaemon.ServerQuery import ServerQuery
from ARKDaemon.ArkServerApi import ArkServerApi

# Load the server configuration
parser = ConfigParser.RawConfigParser()
if os.path.isfile(os.path.join('server.conf')):
    parser.read(os.path.join('server.conf'))
    server_config = parser._sections
    try:
        if server_config['ARK']['mods']:
            mod_list = ast.literal_eval(server_config['ARK']['mods'])
    except KeyError:
        pass

# Initialize the Flask app
app = Flask(__name__)

# Root of the management
@app.route("/")
def root():
    return "Welcome to ARKDaemon"

# API
api_base_uri = '/arkdaemon/api/v1.0'

@app.route("{}/status/".format(api_base_uri), methods=['GET'])
def status():
    this = ServerQuery(ip='127.0.0.1', port=int(server_config['ARK']['query_port']))
    return jsonify(this.status())

# Server operations. Needs an API key for production but I just want to see if it will work
@app.route("{}/operation/start".format(api_base_uri), methods=['GET'])
def start():
    this = ArkServerApi(config=server_config, safe=True)
    return jsonify(this.start())

@app.route("{}/operation/stop".format(api_base_uri), methods=['GET'])
def stop():
    this = ArkServerApi(config=server_config, safe=True)
    return jsonify(this.stop())

if __name__ == "__main__":
    app.debug = True
    app.run()