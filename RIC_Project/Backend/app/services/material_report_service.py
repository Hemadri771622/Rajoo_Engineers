import os
from datetime import datetime, timedelta, timezone
import pandas as pd

from app.services.report_db_service import get_report_db

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable, KeepTogether, PageBreak
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
    os.path.join(BACKEND_DIR, "..", "Frontend", "public", "reports", "material")
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
# HEADER
# =========================================================

def add_header(canvas, doc):
    canvas.saveState()

    current_datetime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Company Title
    canvas.setFont("Helvetica-Bold", 18)
    canvas.setFillColor(colors.HexColor("#0E2F43"))
    canvas.drawString(160, 815, "RAJOO ENGINEERS LTD.")

    canvas.setFont("Helvetica", 11)
    canvas.setFillColor(colors.black)
    canvas.drawString(160, 798, "THREE LAYER BLOWN FILM LINE")
    canvas.drawString(160, 785, "MODEL: RECF-2550-40-1800")

    # Logo
    if os.path.exists(LOGO_PATH):
        canvas.drawImage(
            LOGO_PATH,
            40, 775,
            width=100,
            height=40,
            preserveAspectRatio=True,
            mask='auto'
        )

    # Date
    canvas.drawRightString(560, 785, f"Date & Time : {current_datetime}")

    # Divider
    canvas.setStrokeColor(colors.HexColor("#0FB9B1"))
    canvas.setLineWidth(3)
    canvas.line(40, 770, 560, 770)

    canvas.restoreState()


# =========================================================
# MAIN REPORT FUNCTION
# =========================================================

def generate_material_consumption_pdf(duration_minutes=60):

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=duration_minutes)

    conn = get_report_db()

    df = pd.read_sql_query(
        "SELECT extruder, material_name, total_kg, timestamp FROM material_utilisation",
        conn
    )

    conn.close()

    if df.empty:
        print("No data available.")
        return None

    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df = df[(df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)]

    if df.empty:
        print("No data in selected time window.")
        return None

    # ================= DIFFERENCE CALCULATION =================

    consumption_df = (
        df.groupby(["extruder", "material_name"])
        .agg(min_kg=("total_kg", "min"),
             max_kg=("total_kg", "max"))
        .reset_index()
    )

    consumption_df["consumed_kg"] = (
        consumption_df["max_kg"] - consumption_df["min_kg"]
    )

    final_df = consumption_df[["extruder", "material_name", "consumed_kg"]]

    pivot = final_df.pivot_table(
        index="extruder",
        columns="material_name",
        values="consumed_kg",
        aggfunc="sum",
        fill_value=0
    )

    pivot["Total (KG)"] = pivot.sum(axis=1)

    material_summary = pivot.drop(columns=["Total (KG)"]).sum().reset_index()
    material_summary.columns = ["Material", "Total KG"]

    extruder_comparison = pivot[["Total (KG)"]].reset_index()
    extruder_comparison.columns = ["Extruder", "Total Production (KG)"]

    grand_total = extruder_comparison["Total Production (KG)"].sum()

    highest_extruder = extruder_comparison.sort_values(
        "Total Production (KG)", ascending=False
    ).iloc[0]

    lowest_extruder = extruder_comparison.sort_values(
        "Total Production (KG)"
    ).iloc[0]

    highest_material = material_summary.sort_values(
        "Total KG", ascending=False
    ).iloc[0]

    # ================= PDF CREATION =================

    filename = os.path.join(
        FRONTEND_REPORT_PATH,
        f"material_consumption_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
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

    # ================= TITLE =================

    elements.append(Paragraph("MATERIAL CONSUMPTION REPORT", title_style))
    elements.append(HRFlowable(width="100%", thickness=3,
                               color=colors.HexColor("#0FB9B1")))
    elements.append(Spacer(1, 0.4 * inch))

    # ================= TABLE 1 =================

    elements.append(Paragraph("Total Material Usage (KG)", section_style))
    elements.append(Spacer(1, 0.2 * inch))

    table_data = [["Extruder"] + list(pivot.columns)]

    for idx, row in pivot.iterrows():
        table_data.append([idx] + list(round(val, 2) for val in row))

    table = Table(table_data, repeatRows=1)
    table.hAlign = "CENTER"

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0E2F43")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.5 * inch))

    # ================= TABLE 2 =================

    elements.append(Paragraph("Material Grand Total Summary", section_style))
    elements.append(Spacer(1, 0.2 * inch))

    summary_data = [["Material", "Total KG"]]

    for _, row in material_summary.iterrows():
        summary_data.append([row["Material"], round(row["Total KG"], 2)])

    summary_table = Table(summary_data, repeatRows=1)
    summary_table.hAlign = "CENTER"

    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0FB9B1")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
    ]))

    elements.append(summary_table)
    elements.append(Spacer(1, 0.5 * inch))

    # ================= TABLE 3 =================

    elements.append(Paragraph("Extruder Production Comparison", section_style))
    elements.append(Spacer(1, 0.2 * inch))

    comparison_data = [["Extruder", "Total Production (KG)"]]

    for _, row in extruder_comparison.iterrows():
        comparison_data.append([row["Extruder"],
                                round(row["Total Production (KG)"], 2)])

    comparison_data.append(["Grand Total", round(grand_total, 2)])

    comparison_table = Table(comparison_data, repeatRows=1)
    comparison_table.hAlign = "CENTER"

    comparison_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0E2F43")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('BACKGROUND', (0, len(comparison_data)-1),
         (-1, len(comparison_data)-1),
         colors.HexColor("#FFE8CC")),
    ]))

    elements.append(KeepTogether(comparison_table))

    # ================= PAGE BREAK =================
    elements.append(PageBreak())

    # ================= INSIGHTS =================

    elements.append(Paragraph("Insights", section_style))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(
        f"<b>Highest Producing Extruder:</b> {highest_extruder['Extruder']} – "
        f"{round(highest_extruder['Total Production (KG)'], 2)} KG",
        styles["Normal"]
    ))

    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(
        f"<b>Lowest Producing Extruder:</b> {lowest_extruder['Extruder']} – "
        f"{round(lowest_extruder['Total Production (KG)'], 2)} KG",
        styles["Normal"]
    ))

    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(
        f"<b>Highest Consumed Material:</b> {highest_material['Material']} – "
        f"{round(highest_material['Total KG'], 2)} KG",
        styles["Normal"]
    ))

    # ================= BUILD PDF =================

    doc.build(
        elements,
        onFirstPage=add_header,
        onLaterPages=add_header,
        canvasmaker=NumberedCanvas
    )

    print(f"Professional Material Report generated: {filename}")
    return filename