from flask import Flask, render_template, request, redirect, send_from_directory
import os

app = Flask(__name__)
PHOTO_DIR = "photos"

@app.route("/photos/<filename>")
def photos(filename):
    return send_from_directory(PHOTO_DIR, filename)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        new_time = request.form["alarm_time"]
        with open("alarm.txt", "w") as f:
            f.write(new_time)
        return redirect("/")

    if os.path.exists("alarm.txt"):
        with open("alarm.txt") as f:
            alarm_time = f.read().strip()
    else:
        alarm_time = "07:00"

    return render_template("index.html", alarm_time=alarm_time)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
