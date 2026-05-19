# import sqlite3
# import os

# # =========================================================
# # PATH CONFIGURATION
# # =========================================================

# BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
# INSTANCE_PATH = os.path.join(BACKEND_DIR, "instance")
# REPORT_DB_PATH = os.path.join(INSTANCE_PATH, "report_database.db")


# # =========================================================
# # CONNECTION
# # =========================================================

# def get_report_db():
#     return sqlite3.connect(REPORT_DB_PATH)


# # =========================================================
# # INITIALIZE REPORT DATABASE
# # =========================================================

# def init_report_db():

#     if not os.path.exists(INSTANCE_PATH):
#         raise Exception(f"Instance folder not found at: {INSTANCE_PATH}")

#     print("Report DB path resolved to:", REPORT_DB_PATH)

#     conn = sqlite3.connect(REPORT_DB_PATH)
#     cur = conn.cursor()

#     # ================= PROCESS SUMMARY TABLE =================
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS process_summary (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

#             nominal_thickness REAL,
#             avg_thickness REAL,
#             max_thickness REAL,
#             min_thickness REAL,

#             control_limit REAL,
#             two_sigma REAL,

#             line_speed REAL,
#             gbr_position REAL
#         )
#     """)

#     # ================= MATERIAL UTILISATION TABLE =================
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS material_utilisation (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
#             extruder TEXT NOT NULL,
#             material_name TEXT NOT NULL,
#             total_kg REAL NOT NULL
#         )
#     """)

#     conn.commit()
#     conn.close()



import sqlite3
import os

# =========================================================
# PATH CONFIGURATION
# =========================================================

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INSTANCE_PATH = os.path.join(BACKEND_DIR, "instance")
REPORT_DB_PATH = os.path.join(INSTANCE_PATH, "report_database.db")


# =========================================================
# CONNECTION
# =========================================================

def get_report_db():
    return sqlite3.connect(REPORT_DB_PATH)


# =========================================================
# INITIALIZE REPORT DATABASE
# =========================================================

def init_report_db():

    if not os.path.exists(INSTANCE_PATH):
        raise Exception(f"Instance folder not found at: {INSTANCE_PATH}")

    print("Report DB path resolved to:", REPORT_DB_PATH)

    conn = sqlite3.connect(REPORT_DB_PATH)
    cur = conn.cursor()

    # =====================================================
    #  PROCESS SUMMARY 
    # =====================================================

    cur.execute("""
        CREATE TABLE IF NOT EXISTS process_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            nominal_thickness REAL,
            avg_thickness REAL,
            max_thickness REAL,
            min_thickness REAL,

            control_limit REAL,
            two_sigma REAL,

            line_speed REAL,
            gbr_position REAL
        )
    """)

    # =====================================================
    #  MATERIAL UTILISATION
    # =====================================================

    cur.execute("""
        CREATE TABLE IF NOT EXISTS material_utilisation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            extruder TEXT NOT NULL,
            material_name TEXT NOT NULL,
            total_kg REAL NOT NULL
        )
    """)

    # =====================================================
    #  PRODUCTION SUMMARY 
    # =====================================================

    cur.execute("""
        CREATE TABLE IF NOT EXISTS production_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            total_set_output REAL,
            total_actual_output REAL,

            speed_set REAL,
            speed_actual REAL,

            gsm REAL,
            lay_flat REAL,
            density REAL
        )
    """)

    # =====================================================
    #  LAYER SUMMARY 
    # =====================================================

    cur.execute("""
        CREATE TABLE IF NOT EXISTS layer_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            layer_no INTEGER,
            thickness_set REAL,
            thickness_actual REAL
        )
    """)

    # =====================================================
    # WINDER SUMMARY 
    # =====================================================

    cur.execute("""
        CREATE TABLE IF NOT EXISTS winder_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            winder_no INTEGER,
            roll_length REAL,
            roll_dia REAL
        )
    """)

    conn.commit()
    conn.close()