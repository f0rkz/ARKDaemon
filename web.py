import ConfigParser
import ast
import os

from flask import Flask, jsonify, request, abort

from ARKDaemon.ArkBackup import ArkBackup
from ARKDaemon.ArkServerApi import ArkServerApi
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
    if server_config['ARK_WEB']['ssl_crt'] and server_config['ARK_WEB']['ssl_key']:
        ssl_enabled = True
    else:
        ssl_enabled = False

# Initialize the Flask app
app = Flask(__name__)

print "Starting the web API. Your API key is: {}".format(server_config['ARK_WEB']['api_key'])

# Root of the management
@app.route("/")
def root():
    return "Welcome to ARKDaemon"

# API
api_base_uri = '/api'

@app.route("{}/status/".format(api_base_uri), methods=['GET'])
def status():
    this = ServerQuery(ip='127.0.0.1', port=int(server_config['ARK']['query_port']))
    return jsonify(this.status())

# Server operations. Needs an API key for production but I just want to see if it will work
@app.route("{}/operation/start".format(api_base_uri), methods=['GET'])
def start():
    key_received = request.args.get('key')
    api_key = server_config['ARK_WEB']['api_key']
    if key_received == api_key:
        this = ArkServerApi(config=server_config, safe=True)
        return jsonify(this.start())
    else:
        abort(401)

@app.route("{}/operation/stop".format(api_base_uri), methods=['GET'])
def stop():
    key_received = request.args.get('key')
    api_key = server_config['ARK_WEB']['api_key']
    if key_received == api_key:
        this = ArkServerApi(config=server_config, safe=True)
        return jsonify(this.stop())
    else:
        abort(401)

@app.route("{}/operation/save".format(api_base_uri), methods=['GET'])
def save():
    key_received = request.args.get('key')
    api_key = server_config['ARK_WEB']['api_key']
    if key_received == api_key:
        this = ArkServerApi(config=server_config, safe=True)
        return jsonify(this.save())
    else:
        abort(401)

@app.route("{}/operation/backup".format(api_base_uri))
def backup():
    key_received = request.args.get('key')
    api_key = server_config['ARK_WEB']['api_key']
    if key_received == api_key:
        this = ArkBackup(config=server_config)
        return jsonify(this.do_backup())
    else:
        abort(401)

if __name__ == "__main__":
    # SSL
    if ssl_enabled:
        context = (os.path.join('ssl', server_config['ARK_WEB']['ssl_crt']),
                   os.path.join('ssl', server_config['ARK_WEB']['ssl_key']))
        app.run(host='0.0.0.0', port=server_config['ARK_WEB']['port'], ssl_context = context, threaded=True)
    else:
        app.run(host='0.0.0.0', port=server_config['ARK_WEB']['port'], threaded=True)