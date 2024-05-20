import os
import logging
from flask import Flask, request, send_file, jsonify, render_template

app = Flask(__name__, static_folder='static', template_folder='templates')
BASE_DIR = os.path.expanduser("~")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index.html: {e}")
        return "Internal Server Error", 500

@app.route('/files', methods=['GET'])
def list_files():
    try:
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
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/delete', methods=['POST'])
def delete_file():
    try:
        data = request.get_json()
        file_path = os.path.join(BASE_DIR, data['path'])
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({"message": "File deleted"}), 200
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/download', methods=['GET'])
def download_file():
    try:
        file_path = request.args.get('path')
        abs_path = os.path.join(BASE_DIR, file_path)
        if os.path.exists(abs_path):
            return send_file(abs_path, as_attachment=True)
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        return "Internal Server Error", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
