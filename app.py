import os
from flask import Flask, request, send_from_directory, jsonify, render_template

app = Flask(__name__, static_folder='static', template_folder='templates')
BASE_DIR = os.path.expanduser("~")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/files', methods=['GET'])
def list_files():
    path = request.args.get('path', '')
    abs_path = os.path.join(BASE_DIR, path)
    if not os.path.exists(abs_path):
        return jsonify({"error": "Path does not exist"}), 404
    
    files = []
    for filename in os.listdir(abs_path):
        file_path = os.path.join(abs_path, filename)
        files.append({
            "name": filename,
            "is_dir": os.path.isdir(file_path)
        })
    return jsonify(files)

@app.route('/delete', methods=['POST'])
def delete_file():
    data = request.get_json()
    file_path = os.path.join(BASE_DIR, data['path'])
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"message": "File deleted"}), 200
    else:
        return jsonify({"error": "File not found"}), 404

@app.route('/download', methods=['GET'])
def download_file():
    file_path = request.args.get('path')
    directory = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    return send_from_directory(directory, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

