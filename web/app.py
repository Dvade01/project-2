import os
import configparser

from flask import Flask, render_template, abort

app = Flask(__name__, template_folder='pages')

# Read configuration file
config = configparser.ConfigParser()
config_file = 'credentials.ini'
if not os.path.exists(config_file):
    config_file = 'default.ini'
config.read(config_file)

# Get port number and debug mode from credentials.ini
port = int(config['SERVER']['PORT'])
debug = config['SERVER']['DEBUG'].lower() == 'true'

@app.route("/")
def hello():
    return "UOCIS docker demo!\n"

@app.route('/<path:path>')
def serve_file(path):
    if ".." in path or "~" in path:
        abort(403)

    pages_dir = os.path.join(app.root_path, 'pages')
    file_path = os.path.join(pages_dir, path)
    if os.path.isfile(file_path):
        return send_from_directory(pages_dir, path)
    else:
        abort(404)

@app.errorhandler(403)
def handle_403(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def handle_404(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=debug, host='0.0.0.0', port=port)
