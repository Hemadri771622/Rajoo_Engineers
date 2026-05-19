import os
from datetime import datetime, timedelta, timezone
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from app.services.report_db_service import get_report_db

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable, PageBreak, Image, KeepTogether
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
    os.path.join(BACKEND_DIR, "..", "Frontend", "public", "reports", "production")
)

LOGO_PATH = os.path.abspath(
    os.path.join(BACKEND_DIR, "..", "Frontend", "public", "rajoo_logo.png")
)

os.makedirs(FRONTEND_REPORT_PATH, exist_ok=True)


# =========================================================
# COMMON TABLE STYLE
# =========================================================

def get_standard_table_style():
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0E2F43")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ])


# =========================================================
# PAGE NUMBER
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
# HEADER
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

def generate_production_report(duration_minutes=60):

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=duration_minutes)

    conn = get_report_db()

    prod_df = pd.read_sql_query("SELECT * FROM production_summary", conn)
    process_df = pd.read_sql_query("SELECT * FROM process_summary", conn)
    layer_df = pd.read_sql_query("SELECT * FROM layer_summary", conn)
    winder_df = pd.read_sql_query("SELECT * FROM winder_summary", conn)

    conn.close()

    if prod_df.empty:
        return None

    prod_df["timestamp"] = pd.to_datetime(prod_df["timestamp"], utc=True)
    prod_df = prod_df[(prod_df["timestamp"] >= start_time) & (prod_df["timestamp"] <= end_time)]

    if prod_df.empty:
        return None

    prod_df_sorted = prod_df.sort_values("timestamp")

    # ================= CALCULATIONS =================

    actual_output = prod_df["total_actual_output"].max() - prod_df["total_actual_output"].min()
    target_output = prod_df["total_set_output"].max() - prod_df["total_set_output"].min()

    efficiency = round((actual_output / target_output) * 100, 2) if target_output else 0

    avg_speed_set = round(prod_df["speed_set"].mean(), 2)
    avg_speed_actual = round(prod_df["speed_actual"].mean(), 2)
    avg_gsm = round(prod_df["gsm"].mean(), 2)
    avg_layflat = round(prod_df["lay_flat"].mean(), 2)
    avg_density = round(prod_df["density"].mean(), 3)

    avg_thickness = round(process_df["avg_thickness"].mean(), 2)
    max_thickness = round(process_df["max_thickness"].max(), 2)
    min_thickness = round(process_df["min_thickness"].min(), 2)

    deviation = round(((avg_thickness - process_df["nominal_thickness"].iloc[0])
                       / process_df["nominal_thickness"].iloc[0]) * 100, 2)

    layer_summary = layer_df.groupby("layer_no")["thickness_actual"].mean().round(2)

    winder_summary = winder_df.groupby("winder_no")["roll_length"].max() - \
                     winder_df.groupby("winder_no")["roll_length"].min()

    # ================= CREATE GRAPHS =================

    trend_path = os.path.join(FRONTEND_REPORT_PATH, "prod_trend.png")
    speed_path = os.path.join(FRONTEND_REPORT_PATH, "speed_trend.png")

    plt.figure(figsize=(10, 4))
    plt.plot(prod_df_sorted["timestamp"], prod_df_sorted["total_set_output"], label="Target Output")
    plt.plot(prod_df_sorted["timestamp"], prod_df_sorted["total_actual_output"], label="Actual Output")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(trend_path)
    plt.close()

    plt.figure(figsize=(10, 4))
    plt.plot(prod_df_sorted["timestamp"], prod_df_sorted["speed_set"], label="Speed Set")
    plt.plot(prod_df_sorted["timestamp"], prod_df_sorted["speed_actual"], label="Speed Actual")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(speed_path)
    plt.close()

    # ================= BUILD PDF =================

    filename = os.path.join(
        FRONTEND_REPORT_PATH,
        f"production_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

    doc = SimpleDocTemplate(filename, pagesize=A4,
                            rightMargin=40, leftMargin=40,
                            topMargin=70, bottomMargin=40)

    elements = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
    'TitleStyle',
    parent=styles['Title'],
    fontSize=20,
    textColor=colors.HexColor("#0E2F43"),
    spaceAfter=15,
    alignment=1  # Center align
   )

    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor("#0FB9B1"),
        spaceAfter=10
    )
    

    # ================= MAIN TITLE =================

    elements.append(Paragraph("PRODUCTION REPORT", title_style))
    elements.append(HRFlowable(width="100%", thickness=3,
                            color=colors.HexColor("#0FB9B1")))
    elements.append(Spacer(1, 0.5 * inch))

    
    #  Production Output
    elements.append(Paragraph("Production Output", section_style))
    table1 = Table([
        ["Parameter", "Value"],
        ["Target Production (KG/hr)", round(target_output, 2)],
        ["Actual Production (KG/hr)", round(actual_output, 2)],
        ["Production Efficiency (%)", efficiency]
    ], colWidths=[280, 170])
    table1.setStyle(get_standard_table_style())
    elements.append(table1)
    elements.append(Spacer(1, 0.4 * inch))

    #  Production Trend (KeepTogether FIX)
    elements.append(KeepTogether([
        Paragraph("Production Trend", section_style),
        Spacer(1, 0.2 * inch),
        Image(trend_path, width=6 * inch, height=3 * inch),
        Spacer(1, 0.5 * inch)
    ]))

    #  Line Performance
    elements.append(Paragraph("Line Performance", section_style))
    table2 = Table([
        ["Parameter", "Value"],
        ["Speed Set (mpm)", avg_speed_set],
        ["Speed Actual (mpm)", avg_speed_actual],
        ["Average GSM (g/m²)", avg_gsm],
        ["Layflat Width (mm)", avg_layflat],
        ["Density (g/cm³)", avg_density]
    ], colWidths=[280, 170])
    table2.setStyle(get_standard_table_style())
    elements.append(table2)
    elements.append(Spacer(1, 0.5 * inch))

    #  Line Speed Trend (KeepTogether FIX)
    elements.append(KeepTogether([
        Paragraph("Line Speed Trend", section_style),
        Spacer(1, 0.2 * inch),
        Image(speed_path, width=6 * inch, height=3 * inch),
        Spacer(1, 0.5 * inch)
    ]))

    # Production Quality
    elements.append(Paragraph("Production Quality", section_style))
    table3 = Table([
        ["Parameter", "Value"],
        ["Average Thickness (µm)", avg_thickness],
        ["Maximum Thickness (µm)", max_thickness],
        ["Minimum Thickness (µm)", min_thickness],
        ["Thickness Deviation (%)", deviation]
    ], colWidths=[280, 170])
    table3.setStyle(get_standard_table_style())
    elements.append(table3)
    elements.append(PageBreak())

    # Layer Contribution (NO GRAPH)
    elements.append(Paragraph("Layer Contribution", section_style))
    layer_table = [["Layer", "Avg Thickness (µm)"]]
    for layer, value in layer_summary.items():
        layer_table.append([f"Layer {layer}", value])
    table4 = Table(layer_table, colWidths=[280, 170])
    table4.setStyle(get_standard_table_style())
    elements.append(table4)
    elements.append(Spacer(1, 0.5 * inch))

    #  Winder Summary (Unit Added)
    elements.append(Paragraph("Winder Summary", section_style))
    winder_table = [["Winder", "Roll Length Produced (m)"]]
    for winder, value in winder_summary.items():
        winder_table.append([f"Winder {winder}", round(value, 2)])
    table5 = Table(winder_table, colWidths=[280, 170])
    table5.setStyle(get_standard_table_style())
    elements.append(table5)

    doc.build(elements,
              onFirstPage=add_header,
              onLaterPages=add_header,
              canvasmaker=NumberedCanvas)

    return filename