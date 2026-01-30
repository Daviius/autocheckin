import os
from flask import Flask, render_template, request, Response, jsonify

from web.controller import start_automation, stop_automation
from web.logger import log_queue
from projects.nexira import NexiraProject

# =========================
# ROOT PATH = AUTOCHECKIN_ALL
# =========================

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

app = Flask(
    __name__,
    root_path=ROOT_DIR
)

# =========================
# PROJECTS
# =========================

PROJECTS = {
    "nexira": NexiraProject,
}

# =========================
# ROUTES
# =========================

@app.route("/")
def index():
    return render_template(
        "index.html",
        projects=PROJECTS.keys()
    )

@app.route("/start", methods=["POST"])
def start():
    project = request.form.get("project")
    excel = request.form.get("excel")
    concurrent = int(request.form.get("concurrent", 1))

    start_automation(
        PROJECTS[project],
        excel,
        concurrent
    )

    return jsonify({"status": "started"})

@app.route("/stop", methods=["POST"])
def stop():
    stop_automation()
    return jsonify({"status": "stopped"})

@app.route("/logs")
def logs():
    def stream():
        while True:
            msg = log_queue.get()
            yield f"data: {msg}\n\n"
    return Response(stream(), mimetype="text/event-stream")
