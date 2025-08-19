from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import datetime

app = Flask(__name__)
CORS(app)  # allow Angular on localhost to talk to backend

@app.route("/")
def home():
    return "Hello, Flask! The server is running."
    
# Directory to save signed files
SIGNED_DIR = "signed_docs"
os.makedirs(SIGNED_DIR, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file provided"}), 400
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    # Simulate "signing" by adding metadata
    signed_at = datetime.datetime.utcnow().isoformat() + "Z"
    original_filename = file.filename
    signed_filename = f"{os.path.splitext(original_filename)[0]}-signed.pdf"
    signed_path = os.path.join(SIGNED_DIR, signed_filename)

    # Save the file locally in the signed_docs directory
    file.save(signed_path)

    metadata = {
        "filename": original_filename,
        "signed_at": signed_at
    }

    return jsonify({"message": "File signed", "metadata": metadata}), 200

if __name__ == "__main__":
    app.run(debug=True)