from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, urllib.parse, re

app = Flask(__name__)
CORS(app)  # allow all origins

@app.route("/youtube-url")
def youtube_url():

    song = request.args.get("song","").strip()

    if not song:
        return jsonify({"error":"song required"}),400

    encoded = urllib.parse.quote(song)
    url = f"https://www.youtube.com/results?search_query={encoded}"

    r = requests.get(
        url,
        headers={"User-Agent":"Mozilla/5.0"},
        timeout=10
    )

    ids = re.findall(r"watch\?v=([a-zA-Z0-9_-]{11})", r.text)

    if not ids:
        return jsonify({"error":"no video found"}),404

    video_id = list(dict.fromkeys(ids))[0]

    return jsonify({
        "video_id": video_id,
        "embed": f"https://www.youtube-nocookie.com/embed/{video_id}?autoplay=1"
    })
