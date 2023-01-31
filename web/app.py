import os
import configparser

from flask import Flask, send_from_directory

# Create a Flask application object
app = Flask(__name__)

# Read configuration from two files: credentials.ini and default.ini
config = configparser.ConfigParser()
config.read(['credentials.ini', 'default.ini'])

# Get the value of the 'port' key from the 'app' section of the configuration
port = int(config.get('app', 'port', fallback=5000))

# Get the value of the 'debug' key from the 'app' section of the configuration
debug = config.getboolean('app', 'debug', fallback=True)

# Route for the root URL ("/")
@app.route("/")
def hello():
    return "UOCIS docker demo!\n"

# Route for serving files from the 'pages' directory
@app.route('/<path:path>')
def serve_file(path):
    # Check if the requested path contains any illegal characters
    if ".." in path or "~" in path:
        return send_error(403)

    # Get the path to the 'pages' directory
    pages_dir = os.path.join(app.root_path, 'pages')

    # Get the full path to the requested file
    file_path = os.path.join(pages_dir, path)

    # Check if the file exists
    if os.path.isfile(file_path):
        return send_from_directory(pages_dir, path)
    else:
        return send_error(404)

# Function for sending error pages
def send_error(error_code):
    # Determine the error file to send
    error_file = None

    if error_code == 404:
        error_file = '404.html'
    elif error_code == 403:
        error_file = '403.html'
    else:
        return "", error_code

    # Get the path to the 'pages' directory
    pages_dir = os.path.join(app.root_path, 'pages')

    # Get the full path to the error file
    file_path = os.path.join(pages_dir, error_file)

    # Return the error file with the appropriate error code
    return send_from_directory(pages_dir, error_file), error_code

# Run the application if this script is being executed as the main module
if __name__ == "__main__":
    app.run(debug=debug, host='0.0.0.0', port=port)
