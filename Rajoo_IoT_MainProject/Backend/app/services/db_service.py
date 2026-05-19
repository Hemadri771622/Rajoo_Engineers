import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "instance" / "blownfilm.db"

# =========================================================
# DB CONNECTION
# =========================================================
def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# =========================================================
# DB INIT
# =========================================================
def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS machine_overview (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total_set_output REAL,
        total_actual_output REAL,
        density REAL,
        gsm REAL,
        lay_flat REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS machine_timeseries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tag TEXT,
        value REAL,
        index_no INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# =========================================================
# INSERTS
# =========================================================
def insert_machine_overview(data):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO machine_overview
        (total_set_output, total_actual_output, density, gsm, lay_flat)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["total_set_output"],
        data["total_actual_output"],
        data["density"],
        data["gsm"],
        data["lay_flat"]
    ))
    conn.commit()
    conn.close()


from datetime import datetime  


def insert_timeseries(tag, value, index_no=None):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO machine_timeseries (tag, value, index_no, timestamp)
        VALUES (?, ?, ?, ?)
    """, (
        tag,
        value,
        index_no,
        datetime.now().isoformat(timespec="milliseconds")

    ))

    conn.commit()
    conn.close()



# =========================================================
# FETCH – MACHINE OVERVIEW (KPIs)
# =========================================================
def fetch_machine_overview(limit=1):
    """
    Always return the latest KPI snapshot(s)
    """
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM machine_overview
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# =========================================================
# FETCH – GENERIC TIME SERIES (GRAPHS)
# =========================================================
def fetch_series(tag, limit=30):
    """
    Fetch latest N values for any time-series tag
    """
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT value
        FROM machine_timeseries
        WHERE tag = ?
        ORDER BY id DESC
        LIMIT ?
    """, (tag, limit))

    rows = cur.fetchall()
    conn.close()

    # Old → New (for charts)
    return [r["value"] for r in rows[::-1]]


from datetime import datetime, timedelta


def fetch_series_with_step(tag, step_seconds, limit=30):
    """
    Returns time-aware series for charts
    Uses backend clock + known interval
    Does NOT rely on DB timestamps
    """
    values = fetch_series(tag, limit)

    now = datetime.now()
    start = now - timedelta(seconds=step_seconds * (len(values) - 1))

    return [
        {
            "x": (start + timedelta(seconds=i * step_seconds)).isoformat(timespec="seconds"),
            "y": v
        }
        for i, v in enumerate(values)
    ]


# =========================================================
# FETCH – LATEST VALUE (KPIs)
# =========================================================
def fetch_latest_value(tag):
    """
    Used for KPIs like layer speed, yield, ampere
    """
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT value
        FROM machine_timeseries
        WHERE tag = ?
        ORDER BY id DESC
        LIMIT 1
    """, (tag,))

    row = cur.fetchone()
    conn.close()

    return row["value"] if row else 0


# =========================================================
# FETCH – PROFILES (LIP / MAP)
# =========================================================
def fetch_profile(tag):
    """
    Profiles are overwrite-based, order by index_no
    """
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT index_no, value
        FROM machine_timeseries
        WHERE tag = ?
        ORDER BY index_no ASC
    """, (tag,))

    rows = cur.fetchall()
    conn.close()

    return [{"x": r["index_no"], "y": r["value"]} for r in rows]


# =========================================================
# FETCH – ZONE-WISE (DIE TEMP)
# =========================================================
def fetch_zonewise(tag):
    """
    Zone data is overwrite-based, order by index_no
    """
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT index_no, value
        FROM machine_timeseries
        WHERE tag = ?
        ORDER BY index_no ASC
    """, (tag,))

    rows = cur.fetchall()
    conn.close()
    return rows


# =========================================================
#  FETCH – LAYER KPIs
# =========================================================
def fetch_layer_kpis(layer_id):
    """
    Returns KPIs for a single layer
    """
    return {
        "speed": fetch_latest_value(f"layer_{layer_id}_speed"),
        "yield": fetch_latest_value(f"layer_{layer_id}_yield"),
        "ampere": fetch_latest_value(f"layer_{layer_id}_ampere")
    }

# =========================================================
# FETCH – WINDER KPIs
# =========================================================
def fetch_winder_kpis(winder_id):
    """
    Returns KPIs for a single winder
    """
    return {
        "totalizer": fetch_latest_value(f"winder_{winder_id}_totalizer")
    }

# =========================================================
# FETCH – LAYER GRAPHS
# =========================================================
def fetch_layer_trends(layer_id, limit=30):
    """
    Returns graph data for a single layer
    """
    return {
        "melt_pressure": fetch_series(f"layer_{layer_id}_melt_pressure", limit),
        "melt_temperature": fetch_series(f"layer_{layer_id}_melt_temperature", limit),
        "thickness_set": fetch_series(f"layer_{layer_id}_thickness_set", limit),
        "thickness_actual": fetch_series(f"layer_{layer_id}_thickness_actual", limit),
    }

# =========================================================
# FETCH – WINDER GRAPHS
# =========================================================
# def fetch_winder_trends(winder_id, limit=30):
#     """
#     Returns graph data for a single winder
#     """
#     return {
#         "roll_length": fetch_series(f"winder_{winder_id}_roll_length", limit),
#         "roll_dia": fetch_series(f"winder_{winder_id}_roll_dia", limit),
#     }


def fetch_winder_trends(winder_id, limit=30):
    """
    Returns graph data for a single winder
    GUARANTEES minimum 2 points for Chart.js
    """
    roll_length = fetch_series(f"winder_{winder_id}_roll_length", limit)
    roll_dia = fetch_series(f"winder_{winder_id}_roll_dia", limit)

  
    if len(roll_length) == 0:
        roll_length = [0, 1]
    elif len(roll_length) == 1:
        roll_length = [roll_length[0] - 1, roll_length[0]]

    if len(roll_dia) == 0:
        roll_dia = [0, 1]
    elif len(roll_dia) == 1:
        roll_dia = [roll_dia[0] - 1, roll_dia[0]]

    return {
        "roll_length": roll_length,
        "roll_dia": roll_dia,
    }


# =========================================================
# EXTRUDER HELPERS 
# =========================================================

EXTRUDER_MATERIAL_COLORS = {
    "F18010": "#ff9f1c",
    "LD": "#1e90ff",
    "F19010": "#2ecc71",
    "PPA705": "#e74c3c",
    "MLLD": "#9b59b6"
}

EXTRUDER_ZONES = ["BZ-1", "BZ-3", "ADP", "AD1"]


def fetch_extruder_materials_ui(extruder_id):
    """
    Returns extruder material data exactly as frontend expects
    """
    materials = {}

    for mat, color in EXTRUDER_MATERIAL_COLORS.items():
        materials[mat] = {
            "set": fetch_latest_value(
                f"extruder_{extruder_id}_material_{mat}_set_pct"
            ),
            "act": fetch_latest_value(
                f"extruder_{extruder_id}_material_{mat}_act_pct"
            ),
            "setKg": fetch_latest_value(
                f"extruder_{extruder_id}_material_{mat}_set_kg"
            ),
            "actKg": fetch_latest_value(
                f"extruder_{extruder_id}_material_{mat}_act_kg"
            ),
            "density": fetch_latest_value(
                f"extruder_{extruder_id}_material_{mat}_density"
            ),
            "color": color
        }

    return materials


def fetch_extruder_temperature_ui(extruder_id):
    """
    Returns extruder temperature zones exactly as frontend expects
    """
    return [
        {
            "zone": zone,
            "set": fetch_latest_value(
                f"extruder_{extruder_id}_temp_{zone}_set"
            ),
            "act": fetch_latest_value(
                f"extruder_{extruder_id}_temp_{zone}_act"
            )
        }
        for zone in EXTRUDER_ZONES
    ]


# =========================================================
# FETCH – MATERIAL UTILISATION (TIME SERIES)
# =========================================================

MATERIAL_LIST = ["F18010", "LD", "F19010", "PPA705", "MLLD"]
EXTRUDER_IDS = ["A", "B", "C"]


def fetch_material_utilisation_series(extruder_id, limit=30):
    """
    Returns time-series data for ALL 5 materials
    for a single extruder.

    Output format:
    {
        "F18010": [{"x": timestamp, "y": value}, ...],
        "LD": [...],
        ...
    }
    """

    conn = get_db()
    cur = conn.cursor()

    result = {}

    for mat in MATERIAL_LIST:
        tag = f"material_utilisation_{extruder_id}_{mat}_total_kg"

        cur.execute("""
            SELECT value, timestamp
            FROM machine_timeseries
            WHERE tag = ?
            ORDER BY id DESC
            LIMIT ?
        """, (tag, limit))

        rows = cur.fetchall()

        # Reverse → Old to New for charts
        rows = rows[::-1]

        result[mat] = [
            {
                "x": r["timestamp"],
                "y": r["value"]
            }
            for r in rows
        ]

    conn.close()
    return result


# =========================================================
# FETCH – MATERIAL UTILISATION GRAND TOTAL
# =========================================================

def fetch_material_utilisation_grand_total(extruder_id, limit=30):
    """
    Returns cumulative grand total per extruder.
    Used if you want 3 simple charts instead of 15 lines.
    """

    tag = f"material_utilisation_{extruder_id}_grand_total_kg"

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT value, timestamp
        FROM machine_timeseries
        WHERE tag = ?
        ORDER BY id DESC
        LIMIT ?
    """, (tag, limit))

    rows = cur.fetchall()
    conn.close()

    rows = rows[::-1]

    return [
        {
            "x": r["timestamp"],
            "y": r["value"]
        }
        for r in rows
    ]