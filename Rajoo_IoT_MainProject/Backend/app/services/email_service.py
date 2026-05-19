from pathlib import Path
import smtplib
from email.message import EmailMessage


# =========================================================
# PROJECT ROOT
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[3]

REPORT_BASE = BASE_DIR / "Frontend" / "public" / "reports"

PRODUCTION_FOLDER = REPORT_BASE / "production"
THICKNESS_FOLDER = REPORT_BASE / "thickness"
MATERIAL_FOLDER = REPORT_BASE / "material"


# =========================================================
# EMAIL CONFIG
# =========================================================

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = "hemadri13395@gmail.com"
SENDER_PASSWORD = "dixr fqtq bdcz xrrc"
RECEIVER_EMAIL = "hemadri.hjj.jadeja@ammann.com"


# =========================================================
# GET LATEST FILE FROM FOLDER
# =========================================================

def get_latest_from_folder(folder_path):

    if not folder_path.exists():
        print("[EMAIL] Folder not found:", folder_path)
        return None

    pdf_files = list(folder_path.glob("*.pdf"))

    if not pdf_files:
        print("[EMAIL] No PDF found in:", folder_path)
        return None

    return max(pdf_files, key=lambda f: f.stat().st_mtime)


# =========================================================
# SEND ALL 3 REPORTS
# =========================================================

def send_all_reports():

    production_report = get_latest_from_folder(PRODUCTION_FOLDER)
    thickness_report = get_latest_from_folder(THICKNESS_FOLDER)
    material_report = get_latest_from_folder(MATERIAL_FOLDER)

    attachments = [production_report, thickness_report, material_report]

    # Filter out None
    attachments = [f for f in attachments if f]

    if not attachments:
        print("[EMAIL] No reports available to send")
        return

    msg = EmailMessage()
    msg["Subject"] = "Hourly Production Reports"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    msg.set_content(
        "Please find attached the latest reports:\n\n"
        "- Production Report\n"
        "- Thickness Profile Report\n"
        "- Material Consumption Report"
    )

    for file_path in attachments:
        with open(file_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="pdf",
                filename=file_path.name
            )
        print("[EMAIL] Attached:", file_path.name)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

    print("[EMAIL] All reports sent successfully")