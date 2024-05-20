from flask import Flask, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/files')
def list_files():
    path = request.args.get('path', '')
    abs_path = os.path.join(os.getcwd(), path)
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
    data = request.json
    path = data['path']
    abs_path = os.path.join(os.getcwd(), path)

    if not os.path.exists(abs_path):
        return jsonify({"error": "File or directory not found"}), 404

    try:
        if os.path.isdir(abs_path):
            os.rmdir(abs_path)
        else:
            os.remove(abs_path)
        return jsonify({"message": "Deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download')
def download_file():
    path = request.args.get('path', '')
    abs_path = os.path.join(os.getcwd(), path)

    if not os.path.exists(abs_path):
        return jsonify({"error": "File not found"}), 404

    return send_file(abs_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)



