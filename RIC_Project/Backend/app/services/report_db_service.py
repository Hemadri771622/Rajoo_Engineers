import sqlite3
import os

# =========================================================
# PATH CONFIGURATION
# =========================================================

BACKEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

INSTANCE_PATH = os.path.join(
    BACKEND_DIR,
    "instance"
)

REPORT_DB_PATH = os.path.join(
    INSTANCE_PATH,
    "report_database.db"
)

# =========================================================
# CREATE INSTANCE DIRECTORY
# =========================================================

os.makedirs(

    INSTANCE_PATH,

    exist_ok=True
)

# =========================================================
# CONNECTION
# =========================================================

def get_report_db():

    conn = sqlite3.connect(

        REPORT_DB_PATH,

        check_same_thread=False
    )

    # =====================================================
    # SQLITE PERFORMANCE
    # =====================================================

    conn.execute(
        "PRAGMA journal_mode=WAL;"
    )

    conn.execute(
        "PRAGMA synchronous=NORMAL;"
    )

    return conn


# =========================================================
# INITIALIZE REPORT DATABASE
# =========================================================

def init_report_db():

    print("Report DB path resolved to:", REPORT_DB_PATH)

    conn = get_report_db()

    cur = conn.cursor()

    # =====================================================
    # PROCESS SUMMARY
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

            line_speed_set REAL,
            line_speed_actual REAL,

            gbr_position REAL,

            gsm REAL,
            lay_flat REAL,
            density REAL,

            valve_position REAL,

            set_tower_nip REAL,
            actual_tower_nip REAL,

            set_air_ring REAL,
            actual_air_ring REAL,

            set_regeneration REAL,
            actual_regeneration REAL,

            set_reverse_hauloff REAL,
            actual_reverse_hauloff REAL
        )

    """)

    # =====================================================
    # MATERIAL UTILISATION
    # =====================================================

    cur.execute("""

        CREATE TABLE IF NOT EXISTS material_utilisation (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            extruder TEXT NOT NULL,

            component_no INTEGER,

            material_index INTEGER,

            material_name TEXT NOT NULL,

            density REAL,

            set_pct REAL,
            act_pct REAL,

            set_kg REAL,
            act_kg REAL,

            total_kg REAL,

            deviation REAL
        )

    """)

    # =====================================================
    # PRODUCTION SUMMARY
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

            density REAL,

            thickness_actual REAL
        )

    """)

    # =====================================================
    # LAYER SUMMARY
    # =====================================================

    cur.execute("""

        CREATE TABLE IF NOT EXISTS layer_summary (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            layer_no INTEGER,

            thickness_set REAL,
            thickness_actual REAL,

            flow_rate REAL,

            yield_value REAL,

            ampere REAL,

            melt_pressure REAL,

            melt_temperature REAL
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

            totalizer REAL,

            number_of_rolls REAL,

            roll_length REAL,

            roll_dia REAL
        )

    """)

    # =====================================================
    # EXTRUDER TEMPERATURE SUMMARY
    # =====================================================

    cur.execute("""

        CREATE TABLE IF NOT EXISTS extruder_temperature_summary (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            extruder TEXT,

            zone TEXT,

            actual_temp REAL
        )

    """)

    # =====================================================
    # DIE TEMPERATURE SUMMARY
    # =====================================================

    cur.execute("""

        CREATE TABLE IF NOT EXISTS die_temperature_summary (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            zone TEXT,

            set_temp REAL,

            actual_temp REAL
        )

    """)

    # =====================================================
    # IBC SUMMARY
    # =====================================================

    cur.execute("""

        CREATE TABLE IF NOT EXISTS ibc_summary (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            ibc_in REAL,

            ibc_out REAL
        )

    """)

    # =====================================================
    # THICKNESS SUMMARY
    # =====================================================

    cur.execute("""

        CREATE TABLE IF NOT EXISTS thickness_summary (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            thickness_actual REAL
        )

    """)

    # =====================================================
    # MACHINE SPEED SUMMARY
    # =====================================================

    cur.execute("""

        CREATE TABLE IF NOT EXISTS machine_speed_summary (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            speed_set REAL,

            speed_actual REAL
        )

    """)

    # =====================================================
    # INDEXES
    # =====================================================

    cur.execute("""

        CREATE INDEX IF NOT EXISTS idx_process_summary_timestamp

        ON process_summary(timestamp)

    """)

    cur.execute("""

        CREATE INDEX IF NOT EXISTS idx_material_utilisation_timestamp

        ON material_utilisation(timestamp)

    """)

    cur.execute("""

        CREATE INDEX IF NOT EXISTS idx_production_summary_timestamp

        ON production_summary(timestamp)

    """)

    cur.execute("""

        CREATE INDEX IF NOT EXISTS idx_layer_summary_timestamp

        ON layer_summary(timestamp)

    """)

    cur.execute("""

        CREATE INDEX IF NOT EXISTS idx_winder_summary_timestamp

        ON winder_summary(timestamp)

    """)

    cur.execute("""

        CREATE INDEX IF NOT EXISTS idx_extruder_temperature_summary_timestamp

        ON extruder_temperature_summary(timestamp)

    """)

    cur.execute("""

        CREATE INDEX IF NOT EXISTS idx_die_temperature_summary_timestamp

        ON die_temperature_summary(timestamp)

    """)

    cur.execute("""

        CREATE INDEX IF NOT EXISTS idx_ibc_summary_timestamp

        ON ibc_summary(timestamp)

    """)

    cur.execute("""

        CREATE INDEX IF NOT EXISTS idx_thickness_summary_timestamp

        ON thickness_summary(timestamp)

    """)

    cur.execute("""

        CREATE INDEX IF NOT EXISTS idx_machine_speed_summary_timestamp

        ON machine_speed_summary(timestamp)

    """)

    conn.commit()

    conn.close()

    print("===================================")
    print("REPORT DATABASE INITIALIZED")
    print("===================================")