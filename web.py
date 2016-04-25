import ConfigParser
import ast
import os
import uuid

from flask import Flask, jsonify, request, abort, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap

from ARKDaemon.ArkBackup import ArkBackup
from ARKDaemon.ArkServer import ArkServer
from ARKDaemon.ServerQuery import ServerQuery
from ARKDaemon.SteamCmd import SteamCmd

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
app = Flask(__name__, template_folder=os.path.join('ARKWeb', 'templates'), static_folder=os.path.join('ARKWeb', 'static'))
Bootstrap(app)

app.config['USERNAME'] = server_config['ARK_WEB']['admin_user']
app.config['PASSWORD'] = server_config['ARK_WEB']['admin_pass']
# Generate a random key for the secret.
app.config['SECRET_KEY'] = uuid.uuid4().hex

if server_config['ARK_WEB']['api_key']:
    print "Starting the web API. Your API key is: {}".format(server_config['ARK_WEB']['api_key'])
else:
    print "No API key is set in server.conf. Some features will not work correctly."

# Root of the management
@app.route("/")
def root():
    return render_template('landing.html')

@app.route("/mods")
def mods():
    this = ServerQuery(ip='127.0.0.1', port=int(server_config['ARK']['query_port']), config=server_config)
    server_status = this.status()
    return render_template('mods.html', status=server_status)

@app.route("/dashboard")
def dashboard():
    if session.get('logged_in'):
        this = ServerQuery(ip='127.0.0.1', port=int(server_config['ARK']['query_port']), config=server_config)
        server_status = this.status()
        return render_template('dashboard.html', status=server_status)
    else:
        return render_template('login.html', error="Permission Denied")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('root'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('root'))
    return render_template('login.html', error=error)

# API
api_base_uri = '/api'

@app.route("{}/status/".format(api_base_uri), methods=['GET'])
def status():
    this = ServerQuery(ip='127.0.0.1', port=int(server_config['ARK']['query_port']), config=server_config)
    return jsonify(this.status())

# Server operations. Needs an API key for production but I just want to see if it will work
@app.route("{}/operation/start".format(api_base_uri), methods=['GET'])
def start():
    key_received = request.args.get('key')
    api_key = server_config['ARK_WEB']['api_key']
    if key_received == api_key:
        this = ArkServer(config=server_config, safe=True)
        return jsonify(this.start())
    else:
        abort(401)

@app.route("{}/operation/stop".format(api_base_uri), methods=['GET'])
def stop():
    key_received = request.args.get('key')
    api_key = server_config['ARK_WEB']['api_key']
    if key_received == api_key:
        this = ArkServer(config=server_config, safe=True)
        return jsonify(this.stop())
    else:
        abort(401)

@app.route("{}/operation/save".format(api_base_uri), methods=['GET'])
def save():
    key_received = request.args.get('key')
    api_key = server_config['ARK_WEB']['api_key']
    if key_received == api_key:
        this = ArkServer(config=server_config, safe=True)
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

@app.route("{}/operation/install_steamcmd".format(api_base_uri))
def install_steamcmd():
    key_received = request.args.get('key')
    api_key = server_config['ARK_WEB']['api_key']
    if key_received == api_key:
        this = SteamCmd(appid=server_config['ARK']['appid'])
        return jsonify(this.install_steamcmd())
    else:
        abort(401)

@app.route("{}/operation/update_ark".format(api_base_uri))
def update_ark():
    key_received = request.args.get('key')
    api_key = server_config['ARK_WEB']['api_key']
    if key_received == api_key:
        result = {}
        result['error'] = True
        result['message'] = "Feature in development."
        return jsonify(result)
    else:
        abort(401)

@app.route("{}/operation/install_ark".format(api_base_uri))
def install_ark():
    key_received = request.args.get('key')
    api_key = server_config['ARK_WEB']['api_key']
    if key_received == api_key:
        result = {}
        result['error'] = True
        result['message'] = "Feature in development."
        return jsonify(result)
    else:
        abort(401)

@app.route("{}/operation/install_mod".format(api_base_uri))
def install_mod():
    key_received = request.args.get('key')
    api_key = server_config['ARK_WEB']['api_key']
    if key_received == api_key:
        mod_id = request.args.get('mod_id')
        this = SteamCmd(appid=server_config['ARK']['appid'], mod_id=mod_id)
        return jsonify(this.install_mod())
    else:
        abort(401)

@app.route("{}/operation/update_mods".format(api_base_uri))
def update_mods():
    key_received = request.args.get('key')
    api_key = server_config['ARK_WEB']['api_key']
    if key_received == api_key:
        result = {}
        result['error'] = True
        result['message'] = "Feature in development."
    else:
        abort(401)

if __name__ == "__main__":
    # SSL
    if ssl_enabled:
        context = (os.path.join('ssl', server_config['ARK_WEB']['ssl_crt']),
                   os.path.join('ssl', server_config['ARK_WEB']['ssl_key']))
        app.run(host='0.0.0.0', port=int(server_config['ARK_WEB']['port']), ssl_context=context, threaded=True)
    else:
        app.run(port=int(server_config['ARK_WEB']['port']), host='0.0.0.0', debug=True, threaded=True)
