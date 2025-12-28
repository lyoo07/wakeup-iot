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
    if request.method == "POST":
        new_time = request.form["alarm_time"]
        with open("alarm.txt", "w") as f:
            f.write(new_time)
        return redirect("/")
    
    with open("alarm.txt") as f:
        alarm_time = f.read().strip()
    
    return render_template("index.html", alarm_time=alarm_time)

if __name__ == "_main_":
    app.run(host="0.0.0.0", port=5000)