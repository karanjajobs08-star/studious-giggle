import os
import subprocess
import uuid
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "KANZIS Server is running"})

@app.route("/download")
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    filename = f"/tmp/{uuid.uuid4()}.mp3"
    try:
        subprocess.run([
            "yt-dlp", "-x", "--audio-format", "mp3",
            "-o", filename, url
        ], check=True, timeout=120)
        return send_file(filename, as_attachment=True, download_name="kanzis_song.mp3")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
