from flask import Flask, jsonify
import os

app = Flask(name)

@app.route("/")
def home():
return jsonify({
"status": "success",
"message": "My JWT API is running!"
})

@app.route("/health")
def health():
return jsonify({"status": "ok"})

if name == "main":
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
