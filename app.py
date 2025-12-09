# from flask import Flask, render_template, request, redirect, url_for
# from parser_mod import parse_config
# from checks import run_checks
# import json

# app = Flask(__name__)

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/scan", methods=["POST"])
# def scan():
#     file = request.files.get("config")
#     text = file.read().decode() if file else request.form.get("rawconfig","")
#     cfg = parse_config(text)
#     results = run_checks(cfg)
#     report_json = json.dumps(results, indent=2)
#     return render_template("report.html", results=results, raw=report_json)

# if __name__ == "__main__":
#     app.run(debug=True)







from flask import Flask, render_template, request, redirect, url_for, flash
from parser_mod import parse_config
from checks import run_checks
import json
import time

app = Flask(__name__)
app.secret_key = "change_this_secret_key"  # needed for flash messages


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    try:
        file = request.files.get("config")
        text_area = request.form.get("rawconfig", "").strip()

        config_text = ""

        if file and file.filename:
            raw = file.read()
            try:
                config_text = raw.decode("utf-8", errors="ignore")
            except Exception:
                flash("Could not read file. Please upload a valid text configuration.", "error")
                return redirect(url_for("index"))
        elif text_area:
            config_text = text_area
        else:
            flash("Please upload a config file or paste configuration text.", "error")
            return redirect(url_for("index"))

        if not config_text.strip():
            flash("Configuration is empty. Please provide a valid device config.", "error")
            return redirect(url_for("index"))

        start = time.time()
        cfg = parse_config(config_text)
        issues = run_checks(cfg)
        end = time.time()

        meta = {
            "lines_count": len(cfg.get("raw", [])),
            "scan_time": round(end - start, 4),
            "issues_count": len(issues),
        }

        report_json = json.dumps(
            {"meta": meta, "issues": issues},
            indent=2
        )

        return render_template(
            "report.html",
            results=issues,
            raw_json=report_json,
            meta=meta
        )

    except Exception as e:
        # generic safety net
        print("Error during scan:", e)
        flash("An unexpected error occurred while scanning. Please try again.", "error")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
