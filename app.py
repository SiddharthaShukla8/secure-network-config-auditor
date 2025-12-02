from flask import Flask, render_template, request, redirect, url_for
from parser_mod import parse_config
from checks import run_checks
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    file = request.files.get("config")
    text = file.read().decode() if file else request.form.get("rawconfig","")
    cfg = parse_config(text)
    results = run_checks(cfg)
    report_json = json.dumps(results, indent=2)
    return render_template("report.html", results=results, raw=report_json)

if __name__ == "__main__":
    app.run(debug=True)
