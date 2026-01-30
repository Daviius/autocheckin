import os
from flask import Flask, render_template, request, Response, jsonify
from jinja2 import FileSystemLoader

from web.controller import start_automation, stop_automation
from web.logger import log_queue
from projects.nexira import NexiraProject

# =========================
# ABSOLUTE PATH RESOLUTION
# =========================

# AUTOCHECKIN_ALL/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# =========================
# FLASK APP (EXPLICIT LOADER)
# =========================

app = Flask(__name__)
app.jinja_loader = FileSystemLoader(TEMPLATE_DIR)
app.static_folder = STATIC_DIR

# DEBUG LOG (BẠN SẼ THẤY TRÊN CONSOLE)
print("BASE_DIR     =", BASE_DIR)
print("TEMPLATE_DIR =", TEMPLATE_DIR)
print("STATIC_DIR   =", STATIC_DIR)
print("TEMPLATES    =", os.listdir(TEMPLATE_DIR))

# =========================
# PROJECT REGISTRY
# =========================

PROJECTS = {
    "nexira": NexiraProject,
}

# =========================
# ROUTES
# =========================

@app.route("/", methods=["GET"])
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

    if project not in PROJECTS:
        return jsonify({"error": "Invalid project"}), 400

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

# =========================
# DO NOT RUN DIRECTLY
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
