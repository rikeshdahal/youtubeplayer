from flask import Flask, request, jsonify
import requests, urllib.parse, re

app = Flask(__name__)

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
        "watch": f"https://youtube.com/watch?v={video_id}",
        "embed": f"https://www.youtube-nocookie.com/embed/{video_id}?autoplay=1"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
