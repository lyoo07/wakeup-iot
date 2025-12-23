from flask import Flask, render_template
import os
from flask import send_from_directory

app = Flask(__name__)
PHOTO_DIR = "photos"

@app.route("/photos/<filename>")
def photos(filename):
    return send_from_directory("photos", filename)

@app.route("/")
def index():
    files = sorted(
        os.listdir(PHOTO_DIR),
        reverse=True
    )
    return render_template("index.html", photos=files)

if __name__ == "_main_":
    app.run(host="0.0.0.0", port=5000)