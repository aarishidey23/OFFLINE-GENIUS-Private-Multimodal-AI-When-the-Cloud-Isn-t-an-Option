from flask import Flask, jsonify, request

# Vercel requires a top-level variable named "app"
app = Flask(__name__)

@app.route("/status")
def status():
    return jsonify({
        "online_ready": True,
        "offline_capable": True,
        "privacy_first": True,
        "snapdragon_ready": True
    })

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    # Replace this with your actual inference logic
    answer = f"You asked: {question}"
    return jsonify({"answer": answer})

# IMPORTANT:
# Do NOT include app.run() here — Vercel manages the server process.
