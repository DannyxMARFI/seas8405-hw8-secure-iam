from flask import Flask, jsonify, request
from auth import verify_token
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the public endpoint!"})

@app.route("/protected")
def protected():
    auth_header = request.headers.get("Authorization", None)
    if not auth_header:
        return jsonify({"error": "Missing token"}), 401

    parts = auth_header.split()
    if parts[0].lower() != "bearer" or len(parts) != 2:
        return jsonify({"error": "Invalid token format"}), 401

    token = parts[1]
    try:
        payload = verify_token(token)
        return jsonify({
            "message": "Access granted to protected resource",
            "user": payload.get("preferred_username", "unknown")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
