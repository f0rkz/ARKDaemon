import os
from flask import Flask, jsonify
import ConfigParser

from ARKDaemon.ServerQuery import ServerQuery

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

# JSON Status endpoint
@app.route("/status")
def status():
    this = ServerQuery(ip='127.0.0.1', port=int(server_config['ARK']['query_port']))
    return jsonify(this.status())

if __name__ == "__main__":
    app.run()