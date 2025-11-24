from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder="static")

@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/proxy")
def proxy():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing query"}), 400
    try:
        url = "https://search.sunnah.one/"
        params = {"ver": "2", "q": query}
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
