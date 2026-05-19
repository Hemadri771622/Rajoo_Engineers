# import os
# from datetime import datetime, timedelta, timezone
# import pandas as pd
# import matplotlib
# matplotlib.use("Agg")
# import matplotlib.pyplot as plt

# from app.services.report_db_service import get_report_db

# from reportlab.platypus import (
#     SimpleDocTemplate, Paragraph, Spacer, Table,
#     TableStyle, HRFlowable, Image
# )
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.units import inch
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas as canvas_module


# # =========================================================
# # PATH CONFIGURATION
# # =========================================================

# BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# FRONTEND_REPORT_PATH = os.path.abspath(
#     os.path.join(BACKEND_DIR, "..", "Frontend", "public", "reports", "thickness")
# )

# LOGO_PATH = os.path.abspath(
#     os.path.join(BACKEND_DIR, "..", "Frontend", "public", "rajoo_logo.png")
# )

# os.makedirs(FRONTEND_REPORT_PATH, exist_ok=True)


# # =========================================================
# # PAGE NUMBER CANVAS
# # =========================================================

# class NumberedCanvas(canvas_module.Canvas):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._saved_page_states = []

#     def showPage(self):
#         self._saved_page_states.append(dict(self.__dict__))
#         self._startPage()

#     def save(self):
#         total_pages = len(self._saved_page_states)
#         for state in self._saved_page_states:
#             self.__dict__.update(state)
#             self.draw_page_number(total_pages)
#             super().showPage()
#         super().save()

#     def draw_page_number(self, page_count):
#         page = f"Page {self._pageNumber} of {page_count}"
#         self.setFont("Helvetica", 9)
#         self.drawRightString(560, 25, page)


# # =========================================================
# # HEADER (MATCHING MATERIAL REPORT STYLE)
# # =========================================================

# def add_header(canvas, doc):
#     canvas.saveState()

#     current_datetime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

#     canvas.setFont("Helvetica-Bold", 18)
#     canvas.setFillColor(colors.HexColor("#0E2F43"))
#     canvas.drawString(160, 815, "RAJOO ENGINEERS LTD.")

#     canvas.setFont("Helvetica", 11)
#     canvas.setFillColor(colors.black)
#     canvas.drawString(160, 798, "THREE LAYER BLOWN FILM LINE")
#     canvas.drawString(160, 785, "MODEL: RECF-2550-40-1800")

#     if os.path.exists(LOGO_PATH):
#         canvas.drawImage(LOGO_PATH, 40, 775, width=100, height=40)

#     canvas.drawRightString(560, 785, f"Date & Time : {current_datetime}")

#     canvas.setStrokeColor(colors.HexColor("#0FB9B1"))
#     canvas.setLineWidth(3)
#     canvas.line(40, 770, 560, 770)

#     canvas.restoreState()


# # =========================================================
# # MAIN REPORT FUNCTION
# # =========================================================

# def generate_thickness_profile_pdf(duration_minutes=2):

#     end_time = datetime.now(timezone.utc)
#     start_time = end_time - timedelta(minutes=duration_minutes)

#     conn = get_report_db()
#     df = pd.read_sql_query("SELECT * FROM process_summary", conn)
#     conn.close()

#     if df.empty:
#         return None

#     df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
#     df = df[(df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)]

#     if df.empty:
#         return None

#     # ================= CALCULATIONS =================

#     avg_thickness = round(df["avg_thickness"].mean(), 2)
#     max_thickness = round(df["max_thickness"].max(), 2)
#     min_thickness = round(df["min_thickness"].min(), 2)
#     spread = round(max_thickness - min_thickness, 2)

#     two_sigma_avg = round(df["two_sigma"].mean(), 2)
#     line_speed_avg = round(df["line_speed"].mean(), 2)
#     gbr_avg = round(df["gbr_position"].mean(), 2)

#     control_limit = df["control_limit"].iloc[0]
#     nominal = df["nominal_thickness"].iloc[0]

#     deviation_percent = round(((avg_thickness - nominal) / nominal) * 100, 2)

#     status = "PROCESS STABLE"
#     if abs(deviation_percent) > control_limit:
#         status = "OUT OF CONTROL"

#     # ================= GRAPH =================

#     graph_path = os.path.join(FRONTEND_REPORT_PATH, "temp_trend.png")

#     df["time_str"] = df["timestamp"].dt.strftime("%H:%M:%S")

#     plt.figure(figsize=(10, 4))

#     plt.plot(df["time_str"], df["min_thickness"], label="Min Thickness")
#     plt.plot(df["time_str"], df["avg_thickness"], label="Average Thickness")
#     plt.plot(df["time_str"], df["max_thickness"], label="Max Thickness")

#     upper_control = nominal * (1 + control_limit / 100)
#     lower_control = nominal * (1 - control_limit / 100)

#     plt.axhline(y=nominal, linestyle="--", label="Nominal")
#     plt.axhline(y=upper_control, linestyle="--", label="Upper Control (+5%)")
#     plt.axhline(y=lower_control, linestyle="--", label="Lower Control (-5%)")

#     plt.xlabel("Time")
#     plt.ylabel("Thickness (µm)")
#     plt.title("Thickness Trend")
#     plt.xticks(rotation=90)
#     plt.grid(True)
#     plt.legend()
#     plt.tight_layout()

#     plt.savefig(graph_path)
#     plt.close()

#     # ================= PDF CREATION =================

#     filename = os.path.join(
#         FRONTEND_REPORT_PATH,
#         f"thickness_profile_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
#     )

#     doc = SimpleDocTemplate(
#         filename,
#         pagesize=A4,
#         rightMargin=40,
#         leftMargin=40,
#         topMargin=70,
#         bottomMargin=40
#     )

#     elements = []
#     styles = getSampleStyleSheet()

#     title_style = ParagraphStyle(
#         'TitleStyle',
#         parent=styles['Title'],
#         fontSize=20,
#         textColor=colors.HexColor("#0E2F43"),
#         spaceAfter=15
#     )

#     section_style = ParagraphStyle(
#         'SectionStyle',
#         parent=styles['Heading2'],
#         fontSize=14,
#         textColor=colors.HexColor("#0FB9B1"),
#         spaceAfter=10
#     )

#     elements.append(Paragraph("THICKNESS PROFILE REPORT", title_style))
#     elements.append(HRFlowable(width="100%", thickness=3,
#                                color=colors.HexColor("#0FB9B1")))
#     elements.append(Spacer(1, 0.4 * inch))

#     # ================= SUMMARY TABLE =================

#     table_data = [
#         ["Parameter", "Value"],
#         ["Nominal Thickness (µm)", nominal],
#         ["Average Thickness (µm)", avg_thickness],
#         ["Maximum Thickness (µm)", max_thickness],
#         ["Minimum Thickness (µm)", min_thickness],
#         ["Thickness Spread (µm)", spread],
#         ["2 Sigma Average (%)", two_sigma_avg],
#         ["Line Speed Avg (mpm)", line_speed_avg],
#         ["GBR Position Avg (°)", gbr_avg],
#         ["Deviation (%)", deviation_percent],
#         ["Process Status", status]
#     ]

#     table = Table(table_data, colWidths=[280, 170])
#     table.hAlign = "CENTER"

#     status_color = colors.HexColor("#D4EDDA") if status == "PROCESS STABLE" else colors.HexColor("#F8D7DA")

#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0E2F43")),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
#         ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
#         ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
#         ('BACKGROUND', (0, len(table_data)-1), (-1, len(table_data)-1), status_color),
#     ]))

#     elements.append(Paragraph("Thickness Summary", section_style))
#     elements.append(table)
#     elements.append(Spacer(1, 0.6 * inch))

#     # ================= GRAPH SECTION =================

#     elements.append(Paragraph("Thickness Trend Graph", section_style))
#     elements.append(Spacer(1, 0.2 * inch))
#     elements.append(Image(graph_path, width=6 * inch, height=3 * inch))

#     doc.build(
#         elements,
#         onFirstPage=add_header,
#         onLaterPages=add_header,
#         canvasmaker=NumberedCanvas
#     )

#     return filename




import os
from datetime import datetime, timedelta, timezone
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from app.services.report_db_service import get_report_db

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable, Image
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as canvas_module


# =========================================================
# PATH CONFIGURATION
# =========================================================

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

FRONTEND_REPORT_PATH = os.path.abspath(
    os.path.join(BACKEND_DIR, "..", "Frontend", "public", "reports", "thickness")
)

LOGO_PATH = os.path.abspath(
    os.path.join(BACKEND_DIR, "..", "Frontend", "public", "rajoo_logo.png")
)

os.makedirs(FRONTEND_REPORT_PATH, exist_ok=True)


# =========================================================
# PAGE NUMBER CANVAS
# =========================================================

class NumberedCanvas(canvas_module.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(total_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        page = f"Page {self._pageNumber} of {page_count}"
        self.setFont("Helvetica", 9)
        self.drawRightString(560, 25, page)


# =========================================================
# HEADER (CORPORATE STYLE)
# =========================================================

def add_header(canvas, doc):
    canvas.saveState()

    current_datetime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    canvas.setFont("Helvetica-Bold", 18)
    canvas.setFillColor(colors.HexColor("#0E2F43"))
    canvas.drawString(160, 815, "RAJOO ENGINEERS LTD.")

    canvas.setFont("Helvetica", 11)
    canvas.setFillColor(colors.black)
    canvas.drawString(160, 798, "THREE LAYER BLOWN FILM LINE")
    canvas.drawString(160, 785, "MODEL: RECF-2550-40-1800")

    if os.path.exists(LOGO_PATH):
        canvas.drawImage(LOGO_PATH, 40, 775, width=100, height=40)

    canvas.drawRightString(560, 785, f"Date & Time : {current_datetime}")

    canvas.setStrokeColor(colors.HexColor("#0FB9B1"))
    canvas.setLineWidth(3)
    canvas.line(40, 770, 560, 770)

    canvas.restoreState()


# =========================================================
# MAIN REPORT FUNCTION
# =========================================================

def generate_thickness_profile_pdf(duration_minutes=2):

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=duration_minutes)

    conn = get_report_db()
    df = pd.read_sql_query("SELECT * FROM process_summary", conn)
    conn.close()

    if df.empty:
        return None

    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df = df[(df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)]

    if df.empty:
        return None

    # ================= CALCULATIONS =================

    avg_thickness = round(df["avg_thickness"].mean(), 2)
    max_thickness = round(df["max_thickness"].max(), 2)
    min_thickness = round(df["min_thickness"].min(), 2)
    spread = round(max_thickness - min_thickness, 2)

    two_sigma_avg = round(df["two_sigma"].mean(), 2)
    line_speed_avg = round(df["line_speed"].mean(), 2)
    gbr_avg = round(df["gbr_position"].mean(), 2)

    control_limit = df["control_limit"].iloc[0]
    nominal = df["nominal_thickness"].iloc[0]
    deviation_percent = round(((avg_thickness - nominal) / nominal) * 100, 2)

    # ================= GRAPH =================

    graph_path = os.path.join(FRONTEND_REPORT_PATH, "temp_trend.png")

    df["time_str"] = df["timestamp"].dt.strftime("%H:%M:%S")

    plt.figure(figsize=(10, 4))

    plt.plot(df["time_str"], df["min_thickness"], label="Min Thickness")
    plt.plot(df["time_str"], df["avg_thickness"], label="Average Thickness")
    plt.plot(df["time_str"], df["max_thickness"], label="Max Thickness")

    upper_control = nominal * (1 + control_limit / 100)
    lower_control = nominal * (1 - control_limit / 100)

    plt.axhline(y=nominal, linestyle="--", label="Nominal")
    plt.axhline(y=upper_control, linestyle="--", label="Upper Control (+5%)")
    plt.axhline(y=lower_control, linestyle="--", label="Lower Control (-5%)")

    plt.xlabel("Time")
    plt.ylabel("Thickness (µm)")
    plt.title("Thickness Trend")
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.savefig(graph_path)
    plt.close()

    # ================= PDF CREATION =================

    filename = os.path.join(
        FRONTEND_REPORT_PATH,
        f"thickness_profile_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=70,
        bottomMargin=40
    )

    elements = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontSize=20,
        textColor=colors.HexColor("#0E2F43"),
        spaceAfter=15
    )

    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor("#0FB9B1"),
        spaceAfter=10
    )

    elements.append(Paragraph("THICKNESS PROFILE REPORT", title_style))
    elements.append(HRFlowable(width="100%", thickness=3,
                               color=colors.HexColor("#0FB9B1")))
    elements.append(Spacer(1, 0.4 * inch))

    # ================= SUMMARY TABLE =================

    table_data = [
        ["Parameter", "Value"],
        ["Nominal Thickness (µm)", nominal],
        ["Average Thickness (µm)", avg_thickness],
        ["Maximum Thickness (µm)", max_thickness],
        ["Minimum Thickness (µm)", min_thickness],
        ["Thickness Spread (µm)", spread],
        ["2 Sigma Average (%)", two_sigma_avg],
        ["Line Speed Avg (mpm)", line_speed_avg],
        ["GBR Position Avg (°)", gbr_avg],
        ["Deviation (%)", deviation_percent]
    ]

    table = Table(table_data, colWidths=[280, 170])
    table.hAlign = "CENTER"

    table.setStyle(TableStyle([
    # Header styling
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0E2F43")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

    # Grid
    ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),

    # Center align ALL cells (including header)
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

    # Vertical middle alignment
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))

    elements.append(Paragraph("Thickness Summary", section_style))
    elements.append(table)
    elements.append(Spacer(1, 0.6 * inch))

    # ================= GRAPH SECTION =================

    elements.append(Paragraph("Thickness Trend Graph", section_style))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Image(graph_path, width=6 * inch, height=3 * inch))

    doc.build(
        elements,
        onFirstPage=add_header,
        onLaterPages=add_header,
        canvasmaker=NumberedCanvas
    )

    return filename