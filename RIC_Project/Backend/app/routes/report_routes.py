import os
from flask import Blueprint, jsonify

report_bp = Blueprint("report_bp", __name__)

# =========================================================
# PATH CONFIGURATION
# =========================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

REPORT_ROOT = os.path.join(
    BASE_DIR,
    "Frontend",
    "public",
    "reports"
)

ALLOWED_TYPES = {"production", "thickness", "material"}


# =========================================================
# GET LATEST FILE
# =========================================================

def get_latest_file(folder_name):

    if folder_name not in ALLOWED_TYPES:
        return None

    folder_path = os.path.join(REPORT_ROOT, folder_name)

    if not os.path.isdir(folder_path):
        print(f"[API] Folder not found: {folder_path}")
        return None

    pdf_files = [
        f for f in os.listdir(folder_path)
        if f.lower().endswith(".pdf")
    ]

    if not pdf_files:
        print(f"[API] No PDF found in {folder_name}")
        return None

    latest_file = max(
        pdf_files,
        key=lambda f: os.path.getmtime(
            os.path.join(folder_path, f)
        )
    )

    return f"/reports/{folder_name}/{latest_file}"


# =========================================================
# ROUTE
# =========================================================

@report_bp.route("/api/latest/<report_type>")
def latest_report(report_type):

    report_type = report_type.lower()

    if report_type not in ALLOWED_TYPES:
        return jsonify({"path": None})

    latest_path = get_latest_file(report_type)

    return jsonify({"path": latest_path})