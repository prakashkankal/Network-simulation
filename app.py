from flask import Flask, send_from_directory, request, render_template_string, jsonify
import os

app = Flask(__name__, static_folder='.')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def read_template(name):
    path = os.path.join(BASE_DIR, name)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/index.html')
def index_html():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/choose')
@app.route('/choose.html')
def choose():
    return send_from_directory(BASE_DIR, 'choose.html')

# Render config.html dynamically with 'algo' variable
@app.route('/config/<algo>')
def config_algo(algo):
    tpl = read_template('config.html')
    return render_template_string(tpl, algo=algo)

# Backwards-compatible: config.html?algo=...
@app.route('/config.html')
def config_query():
    algo = request.args.get('algo', 'link_state')
    tpl = read_template('config.html')
    return render_template_string(tpl, algo=algo)

# Serve other static files (css, images, js) from the same folder
@app.route('/<path:filename>')
def static_files(filename):
    # prevent directory traversal
    safe_path = os.path.normpath(filename)
    if '..' in safe_path.split(os.path.sep):
        return 'Forbidden', 403
    full = os.path.join(BASE_DIR, safe_path)
    if os.path.isfile(full):
        return send_from_directory(BASE_DIR, safe_path)
    return 'Not Found', 404

# Minimal stub for generate_simulation to avoid JS fetch errors (returns 501)
@app.route('/generate_simulation', methods=['POST'])
def generate_simulation():
    return jsonify({"error": "Not implemented on server. Simulation will use client-side fallback."}), 501

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
