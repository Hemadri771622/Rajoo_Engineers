import os
from datetime import datetime, timedelta, timezone
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sqlite3

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    PageBreak,
    Image
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as canvas_module


# =========================================================
# PATH CONFIG
# =========================================================

BACKEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DB_PATH = os.path.join(
    BACKEND_DIR,
    "instance",
    "report_database.db"
)

FRONTEND_REPORT_PATH = os.path.abspath(
    os.path.join(
        BACKEND_DIR,
        "..",
        "Frontend",
        "public",
        "reports",
        "production"
    )
)

LOGO_PATH = os.path.abspath(
    os.path.join(
        BACKEND_DIR,
        "..",
        "Frontend",
        "public",
        "rajoo_logo.png"
    )
)

os.makedirs(
    FRONTEND_REPORT_PATH,
    exist_ok=True
)


# =========================================================
# TABLE STYLE
# =========================================================

def get_standard_table_style():

    return TableStyle([

        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0E2F43")),

        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),

        ('TOPPADDING', (0, 0), (-1, 0), 8),

        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),

        ('TOPPADDING', (0, 1), (-1, -1), 6)

    ])


# =========================================================
# PAGE NUMBER
# =========================================================

class NumberedCanvas(canvas_module.Canvas):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._saved_page_states = []

    def showPage(self):

        self._saved_page_states.append(
            dict(self.__dict__)
        )

        self._startPage()

    def save(self):

        total_pages = len(self._saved_page_states)

        for state in self._saved_page_states:

            self.__dict__.update(state)

            self.draw_page_number(total_pages)

            super().showPage()

        super().save()

    def draw_page_number(self, page_count):

        self.setFont("Helvetica", 9)

        self.drawCentredString(
            300,
            25,
            f"Page {self._pageNumber} of {page_count}"
        )


# =========================================================
# HEADER
# =========================================================

def add_header(canvas, doc):

    canvas.saveState()

    current_datetime = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    canvas.setFont("Helvetica-Bold", 20)

    canvas.setFillColor(
        colors.HexColor("#0E2F43")
    )

    canvas.drawCentredString(
        300,
        815,
        "RAJOO ENGINEERS LTD."
    )

    canvas.setFont("Helvetica", 12)

    canvas.setFillColor(colors.black)

    canvas.drawCentredString(
        300,
        797,
        "THREE LAYER BLOWN FILM LINE"
    )

    canvas.drawCentredString(
        300,
        782,
        "MODEL: RECF-2550-40-1800"
    )

    if os.path.exists(LOGO_PATH):

        canvas.drawImage(
            LOGO_PATH,
            40,
            775,
            width=90,
            height=40,
            preserveAspectRatio=True
        )

    canvas.drawRightString(
        550,
        792,
        f"Date & Time : {current_datetime}"
    )

    canvas.setStrokeColor(
        colors.HexColor("#0FB9B1")
    )

    canvas.setLineWidth(2)

    canvas.line(
        40,
        770,
        555,
        770
    )

    canvas.restoreState()


# =========================================================
# MAIN REPORT
# =========================================================

def generate_production_report():

    try:

        # =================================================
        # TIME RANGE
        # =================================================

        now = datetime.now(timezone.utc)

        end_time = now.replace(
            minute=0,
            second=0,
            microsecond=0
        )

        start_time = end_time - timedelta(hours=1)

        # =================================================
        # DATABASE
        # =================================================

        conn = sqlite3.connect(DB_PATH)

        prod_df = pd.read_sql_query(
            "SELECT * FROM production_summary",
            conn
        )

        process_df = pd.read_sql_query(
            "SELECT * FROM process_summary",
            conn
        )

        ibc_df = pd.read_sql_query(
            "SELECT * FROM ibc_summary",
            conn
        )

        conn.close()

        if prod_df.empty:
            return None

        # =================================================
        # FILTER
        # =================================================

        def filter_df(df):

            df["timestamp"] = pd.to_datetime(
                df["timestamp"],
                utc=True
            )

            return df[
                (df["timestamp"] >= start_time)
                &
                (df["timestamp"] < end_time)
            ]

        prod_df = filter_df(prod_df)

        process_df = filter_df(process_df)

        ibc_df = filter_df(ibc_df)

        if prod_df.empty:
            return None

        prod_df_sorted = prod_df.sort_values(
            "timestamp"
        )

        # =================================================
        # CALCULATIONS
        # =================================================

        actual_output = (
            prod_df["total_actual_output"].max()
            -
            prod_df["total_actual_output"].min()
        )

        target_output = (
            prod_df["total_set_output"].max()
            -
            prod_df["total_set_output"].min()
        )

        efficiency = round(
            (actual_output / target_output) * 100,
            2
        ) if target_output else 0

        avg_speed_set = round(
            prod_df["speed_set"].mean(),
            2
        )

        avg_speed_actual = round(
            prod_df["speed_actual"].mean(),
            2
        )

        avg_gsm = round(
            prod_df["gsm"].mean(),
            2
        )

        avg_layflat = round(
            prod_df["lay_flat"].mean(),
            2
        )

        avg_density = round(
            prod_df["density"].mean(),
            3
        )

        # =================================================
        # GRAPH FILES
        # =================================================

        timestamp_str = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        trend_path = os.path.join(
            FRONTEND_REPORT_PATH,
            f"prod_trend_{timestamp_str}.png"
        )

        speed_path = os.path.join(
            FRONTEND_REPORT_PATH,
            f"speed_trend_{timestamp_str}.png"
        )

        # =================================================
        # PRODUCTION TREND GRAPH
        # =================================================

        plt.figure(figsize=(10, 4))

        plt.plot(
            prod_df_sorted["timestamp"],
            prod_df_sorted["total_set_output"],
            label="Target Output"
        )

        plt.plot(
            prod_df_sorted["timestamp"],
            prod_df_sorted["total_actual_output"],
            label="Actual Output"
        )

        plt.legend()

        plt.xticks(rotation=45, ha='right')

        plt.tight_layout()

        plt.savefig(trend_path)

        plt.close()

        # =================================================
        # SPEED TREND GRAPH
        # =================================================

        plt.figure(figsize=(10, 4))

        plt.plot(
            prod_df_sorted["timestamp"],
            prod_df_sorted["speed_set"],
            label="Speed Set"
        )

        plt.plot(
            prod_df_sorted["timestamp"],
            prod_df_sorted["speed_actual"],
            label="Speed Actual"
        )

        plt.legend()

        plt.xticks(rotation=45, ha='right')

        plt.tight_layout()

        plt.savefig(speed_path)

        plt.close()

        # =================================================
        # PDF FILE
        # =================================================

        filename = os.path.join(
            FRONTEND_REPORT_PATH,
            f"production_report_{start_time.strftime('%H%M')}_{end_time.strftime('%H%M')}.pdf"
        )

        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=55,
            leftMargin=55,
            topMargin=70,
            bottomMargin=40
        )

        elements = []

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Title'],
            fontSize=18,
            textColor=colors.HexColor("#0E2F43"),
            alignment=1,
            spaceAfter=12
        )

        section_style = ParagraphStyle(
            'SectionStyle',
            parent=styles['Heading2'],
            fontSize=13,
            textColor=colors.HexColor("#008B8B"),
            spaceAfter=8
        )

        # =================================================
        # TITLE
        # =================================================

        elements.append(
            Paragraph(
                f"PRODUCTION REPORT ({start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')})",
                title_style
            )
        )

        elements.append(
            HRFlowable(
                width="100%",
                thickness=2,
                color=colors.HexColor("#0FB9B1")
            )
        )

        elements.append(
            Spacer(1, 0.3 * inch)
        )

        # =================================================
        # PRODUCTION OUTPUT
        # =================================================

        elements.append(
            Paragraph(
                "1. PRODUCTION OUTPUT",
                section_style
            )
        )

        table1 = Table([

            ["Parameter", "Value"],

            ["Target Production (KG/hr)", round(target_output, 2)],

            ["Actual Production (KG/hr)", round(actual_output, 2)],

            ["Production Efficiency (%)", efficiency]

        ], colWidths=[250, 250])

        table1.hAlign = "CENTER"

        table1.setStyle(
            get_standard_table_style()
        )

        elements.append(table1)

        elements.append(
            Spacer(1, 0.25 * inch)
        )

        # =================================================
        # PRODUCTION TREND
        # =================================================

        elements.append(
            Paragraph(
                "2. PRODUCTION TREND",
                section_style
            )
        )

        trend_img = Image(
            trend_path,
            width=6.2 * inch,
            height=2.9 * inch
        )

        trend_img.hAlign = "CENTER"

        elements.append(trend_img)

        elements.append(
            Spacer(1, 0.3 * inch)
        )

        # =================================================
        # LINE PERFORMANCE
        # =================================================

        elements.append(
            Paragraph(
                "3. LINE PERFORMANCE",
                section_style
            )
        )

        table2 = Table([

            ["Parameter", "Value"],

            ["Speed Set (mpm)", avg_speed_set],

            ["Speed Actual (mpm)", avg_speed_actual],

            ["Average GSM (g/m²)", avg_gsm],

            ["Layflat Width (mm)", avg_layflat],

            ["Density (g/cm³)", avg_density]

        ], colWidths=[250, 250])

        table2.hAlign = "CENTER"

        table2.setStyle(
            get_standard_table_style()
        )

        elements.append(table2)

        elements.append(
            Spacer(1, 0.3 * inch)
        )

        # =================================================
        # MACHINE CONTROL PARAMETERS
        # =================================================

        elements.append(
            Paragraph(
                "4. MACHINE CONTROL PARAMETERS",
                section_style
            )
        )

        control_table = Table([

            ["Parameter", "Average Value"],

            ["Valve Position", round(process_df["valve_position"].mean(), 2)],

            ["Tower Nip Set", round(process_df["set_tower_nip"].mean(), 2)],

            ["Tower Nip Actual", round(process_df["actual_tower_nip"].mean(), 2)],

            ["Air Ring Set", round(process_df["set_air_ring"].mean(), 2)],

            ["Air Ring Actual", round(process_df["actual_air_ring"].mean(), 2)],

            ["Regeneration Set", round(process_df["set_regeneration"].mean(), 2)],

            ["Regeneration Actual", round(process_df["actual_regeneration"].mean(), 2)],

            ["Reverse Haul-off Set", round(process_df["set_reverse_hauloff"].mean(), 2)],

            ["Reverse Haul-off Actual", round(process_df["actual_reverse_hauloff"].mean(), 2)]

        ], colWidths=[250, 250])

        control_table.hAlign = "CENTER"

        control_table.setStyle(
            get_standard_table_style()
        )

        elements.append(control_table)

        elements.append(PageBreak())

        # =================================================
        # SPEED TREND
        # =================================================

        elements.append(
            Paragraph(
                "5. LINE SPEED TREND",
                section_style
            )
        )

        speed_img = Image(
            speed_path,
            width=6.2 * inch,
            height=2.9 * inch
        )

        speed_img.hAlign = "CENTER"

        elements.append(speed_img)

        elements.append(
            Spacer(1, 0.3 * inch)
        )

        # =================================================
        # IBC TEMPERATURE SUMMARY
        # =================================================

        elements.append(
            Paragraph(
                "6. IBC TEMPERATURE SUMMARY",
                section_style
            )
        )

        ibc_table = Table([

            ["Parameter", "Average Value"],

            ["IBC In Temperature (°C)", round(ibc_df["ibc_in"].mean(), 2)],

            ["IBC Out Temperature (°C)", round(ibc_df["ibc_out"].mean(), 2)]

        ], colWidths=[250, 250])

        ibc_table.hAlign = "CENTER"

        ibc_table.setStyle(
            get_standard_table_style()
        )

        elements.append(ibc_table)

        # =================================================
        # BUILD PDF
        # =================================================

        doc.build(
            elements,
            onFirstPage=add_header,
            onLaterPages=add_header,
            canvasmaker=NumberedCanvas
        )

        # =================================================
        # CLEANUP
        # =================================================

        if os.path.exists(trend_path):
            os.remove(trend_path)

        if os.path.exists(speed_path):
            os.remove(speed_path)

        print("Production report generated:", filename)

        return filename

    except Exception as e:

        print("Production Report Error:", e)

        return None