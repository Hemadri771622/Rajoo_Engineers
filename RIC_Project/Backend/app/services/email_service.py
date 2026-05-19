# from pathlib import Path
# import smtplib
# from email.message import EmailMessage


# # =========================================================
# # PROJECT ROOT
# # =========================================================

# BASE_DIR = Path(__file__).resolve().parents[3]

# REPORT_BASE = BASE_DIR / "Frontend" / "public" / "reports"

# PRODUCTION_FOLDER = REPORT_BASE / "production"
# THICKNESS_FOLDER = REPORT_BASE / "thickness"
# MATERIAL_FOLDER = REPORT_BASE / "material"


# # =========================================================
# # EMAIL CONFIG
# # =========================================================

# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587

# SENDER_EMAIL = "hemadri13395@gmail.com"
# SENDER_PASSWORD = "dixr fqtq bdcz xrrc"
# RECEIVER_EMAIL = "hemadri.hjj.jadeja@ammann.com"


# # =========================================================
# # GET LATEST FILE FROM FOLDER
# # =========================================================

# def get_latest_from_folder(folder_path):

#     if not folder_path.exists():
#         print("[EMAIL] Folder not found:", folder_path)
#         return None

#     pdf_files = list(folder_path.glob("*.pdf"))

#     if not pdf_files:
#         print("[EMAIL] No PDF found in:", folder_path)
#         return None

#     return max(pdf_files, key=lambda f: f.stat().st_mtime)


# # =========================================================
# # SEND ALL 3 REPORTS
# # =========================================================

# def send_all_reports():

#     production_report = get_latest_from_folder(PRODUCTION_FOLDER)
#     thickness_report = get_latest_from_folder(THICKNESS_FOLDER)
#     material_report = get_latest_from_folder(MATERIAL_FOLDER)

#     attachments = [production_report, thickness_report, material_report]

#     # Filter out None
#     attachments = [f for f in attachments if f]

#     if not attachments:
#         print("[EMAIL] No reports available to send")
#         return

#     msg = EmailMessage()
#     msg["Subject"] = "Hourly Production Reports"
#     msg["From"] = SENDER_EMAIL
#     msg["To"] = RECEIVER_EMAIL

#     msg.set_content(
#         "Please find attached the latest reports:\n\n"
#         "- Production Report\n"
#         "- Thickness Profile Report\n"
#         "- Material Consumption Report"
#     )

#     for file_path in attachments:
#         with open(file_path, "rb") as f:
#             msg.add_attachment(
#                 f.read(),
#                 maintype="application",
#                 subtype="pdf",
#                 filename=file_path.name
#             )
#         print("[EMAIL] Attached:", file_path.name)

#     with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#         server.starttls()
#         server.login(SENDER_EMAIL, SENDER_PASSWORD)
#         server.send_message(msg)

#     print("[EMAIL] All reports sent successfully")






from pathlib import Path
import smtplib
import os
from email.message import EmailMessage
from datetime import datetime, timedelta


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

SENDER_EMAIL = "starksense1325@gmail.com"

SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")

if not SENDER_PASSWORD:
    raise ValueError("Email password not set. Check your config.")


RECEIVER_EMAILS = [
    "Production@rajooic.com",
    "qca@rajooic.com",
    "ukdoshi@rajoo.com",
    "chintan@essenspeciality.com",
    "urdoshi@rajooic.com"
]


# =========================================================
# GET LATEST FILE
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
# SEND REPORTS
# =========================================================

def send_all_reports():

    # LAST COMPLETED HOUR LOGIC
    now = datetime.now()

    end_time_dt = now.replace(minute=0, second=0, microsecond=0)
    start_time_dt = end_time_dt - timedelta(hours=1)

    start_time = start_time_dt.strftime("%d %b %Y, %I:%M %p")
    end_time = end_time_dt.strftime("%d %b %Y, %I:%M %p")

    print(f"[EMAIL] Sending report for: {start_time} → {end_time}")

    # ---- Get reports ----
    production_report = get_latest_from_folder(PRODUCTION_FOLDER)
    thickness_report = get_latest_from_folder(THICKNESS_FOLDER)
    material_report = get_latest_from_folder(MATERIAL_FOLDER)

    # ---- Validate correct hour (YOUR IMPROVEMENT) ----
    expected_hour = start_time_dt.strftime("%H%M")

    if production_report and expected_hour not in production_report.name:
        print(f"[WARNING] Production report may not match expected hour: {expected_hour}")

    if thickness_report and expected_hour not in thickness_report.name:
        print(f"[WARNING] Thickness report may not match expected hour: {expected_hour}")

    if material_report and expected_hour not in material_report.name:
        print(f"[WARNING] Material report may not match expected hour: {expected_hour}")

    # ---- Prepare attachments ----
    attachments = [production_report, thickness_report, material_report]
    attachments = [f for f in attachments if f]

    if not attachments:
        print("[EMAIL] No reports available to send")
        return

    # ---- Create email ----
    msg = EmailMessage()
    msg["Subject"] = f"Production Report ({start_time} - {end_time})"
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(RECEIVER_EMAILS)

    msg.set_content(
        f"""Hello,

Please find attached the hourly reports.

Report Duration:
From: {start_time}
To:   {end_time}

Reports Included:
- Production Report
- Thickness Profile Report
- Material Consumption Report

Regards,
IoT System
"""
    )

    # ---- Attach files ----
    for file_path in attachments:
        try:
            with open(file_path, "rb") as f:
                msg.add_attachment(
                    f.read(),
                    maintype="application",
                    subtype="pdf",
                    filename=file_path.name
                )
            print("[EMAIL] Attached:", file_path.name)
        except Exception as e:
            print(f"[EMAIL ERROR] Failed to attach {file_path.name}: {str(e)}")

    # ---- Send email ----
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg, to_addrs=RECEIVER_EMAILS)

        print("[EMAIL] Reports sent successfully")

    except Exception as e:
        print("[EMAIL ERROR]:", str(e))