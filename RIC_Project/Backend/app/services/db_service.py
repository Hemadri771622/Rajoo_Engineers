import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parents[2] / "instance" / "blownfilm.db"

# =========================================================
# CREATE DB DIRECTORY
# =========================================================

DB_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

# =========================================================
# DB CONNECTION
# =========================================================

def get_db():

    conn = sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

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
# DB INIT
# =========================================================

def init_db():

    conn = get_db()

    cur = conn.cursor()

    # =====================================================
    # MACHINE OVERVIEW
    # =====================================================

    cur.execute("""

    CREATE TABLE IF NOT EXISTS machine_overview (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        total_set_output REAL,
        total_actual_output REAL,

        density REAL,
        gsm REAL,
        lay_flat REAL,

        valve_position REAL,

        set_tower_nip REAL,
        actual_tower_nip REAL,

        set_air_ring REAL,
        actual_air_ring REAL,

        set_regeneration REAL,
        actual_regeneration REAL,

        set_reverse_hauloff REAL,
        actual_reverse_hauloff REAL,

        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )

    """)

    # =====================================================
    # UNIVERSAL HISTORIAN
    # =====================================================

    cur.execute("""

    CREATE TABLE IF NOT EXISTS machine_timeseries (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        tag TEXT,

        value REAL,

        index_no INTEGER,

        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )

    """)

    # =====================================================
    # INDEX FOR PERFORMANCE
    # =====================================================

    cur.execute("""

    CREATE INDEX IF NOT EXISTS idx_machine_timeseries_tag

    ON machine_timeseries(tag)

    """)

    conn.commit()

    conn.close()


# =========================================================
# INSERT – GENERIC TIMESERIES
# =========================================================

def insert_timeseries(tag, value, index_no=None):

    conn = None

    try:

        conn = get_db()

        cur = conn.cursor()

        cur.execute("""

            INSERT INTO machine_timeseries (

                tag,
                value,
                index_no,
                timestamp

            )

            VALUES (?, ?, ?, ?)

        """, (

            tag,
            value,
            index_no,

            datetime.now().isoformat(
                timespec="milliseconds"
            )

        ))

        conn.commit()

    except Exception as e:

        print(
            f"DB INSERT FAILED -> {tag} -> {e}"
        )

    finally:

        if conn:

            conn.close()


# =========================================================
# INSERT – MACHINE OVERVIEW
# =========================================================

def insert_machine_overview(data):

    conn = None

    try:

        conn = get_db()

        cur = conn.cursor()

        cur.execute("""

            INSERT INTO machine_overview (

                total_set_output,
                total_actual_output,

                density,
                gsm,
                lay_flat,

                valve_position,

                set_tower_nip,
                actual_tower_nip,

                set_air_ring,
                actual_air_ring,

                set_regeneration,
                actual_regeneration,

                set_reverse_hauloff,
                actual_reverse_hauloff

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        """, (

            data["total_set_output"],
            data["total_actual_output"],

            data["density"],
            data["gsm"],
            data["lay_flat"],

            data["valve_position"],

            data["set_tower_nip"],
            data["actual_tower_nip"],

            data["set_air_ring"],
            data["actual_air_ring"],

            data["set_regeneration"],
            data["actual_regeneration"],

            data["set_reverse_hauloff"],
            data["actual_reverse_hauloff"]

        ))

        conn.commit()

    except Exception as e:

        print(
            f"MACHINE INSERT FAILED -> {e}"
        )

    finally:

        if conn:

            conn.close()


# =========================================================
# MACHINE TRENDS
# =========================================================

def insert_machine_trends(

    speed_set,
    speed_actual,
    thickness

):

    insert_timeseries(
        "speed_set",
        speed_set
    )

    insert_timeseries(
        "speed_actual",
        speed_actual
    )

    insert_timeseries(
        "thickness_actual",
        thickness
    )


# =========================================================
# IBC DATA
# =========================================================

def insert_ibc_data(

    ibc_in,
    ibc_out

):

    insert_timeseries(
        "ibc_in",
        ibc_in
    )

    insert_timeseries(
        "ibc_out",
        ibc_out
    )


# =========================================================
# DIE TEMPERATURES
# =========================================================

def insert_die_temperatures(zones):

    for zone in zones:

        insert_timeseries(
            f"die_temp_{zone['zone']}_set",
            zone["set"]
        )

        insert_timeseries(
            f"die_temp_{zone['zone']}_actual",
            zone["actual"]
        )


# =========================================================
# LAYER SNAPSHOT
# =========================================================

def insert_layer_snapshot(layer_id, data):

    insert_timeseries(
        f"layer_{layer_id}_speed",
        data["speed"]
    )

    insert_timeseries(
        f"layer_{layer_id}_yield",
        data["yield"]
    )

    insert_timeseries(
        f"layer_{layer_id}_ampere",
        data["ampere"]
    )

    insert_timeseries(
        f"layer_{layer_id}_melt_pressure",
        data["melt_pressure"]
    )

    insert_timeseries(
        f"layer_{layer_id}_melt_temperature",
        data["melt_temperature"]
    )


# =========================================================
# LAYER TRENDS
# =========================================================

def insert_layer_trends(layer_id, trends):

    insert_timeseries(
        f"layer_{layer_id}_flow_rate",
        trends["flow_rate"][-1]
    )

    insert_timeseries(
        f"layer_{layer_id}_yield_trend",
        trends["yield"][-1]
    )

    insert_timeseries(
        f"layer_{layer_id}_thickness",
        trends["thickness"][-1]
    )


# =========================================================
# WINDER SNAPSHOT
# =========================================================

def insert_winder_snapshot(winder_id, data):

    insert_timeseries(
        f"winder_{winder_id}_totalizer",
        data["totalizer"]
    )

    insert_timeseries(
        f"winder_{winder_id}_number_of_rolls",
        data["number_of_rolls"]
    )

    insert_timeseries(
        f"winder_{winder_id}_roll_length_live",
        data["roll_length_live"]
    )

    insert_timeseries(
        f"winder_{winder_id}_roll_diameter_live",
        data["roll_diameter_live"]
    )


# =========================================================
# WINDER TRENDS
# =========================================================

def insert_winder_trends(winder_id, trends):

    insert_timeseries(
        f"winder_{winder_id}_roll_length",
        trends["roll_length"][-1]
    )

    insert_timeseries(
        f"winder_{winder_id}_roll_dia",
        trends["roll_dia"][-1]
    )


# =========================================================
# EXTRUDER SNAPSHOT
# =========================================================

def insert_extruder_snapshot(extruder_id, data):

    for comp in data["components"]:

        component = comp["component"]

        insert_timeseries(
            f"extruder_{extruder_id}_component_{component}_material_index",
            comp["material_index"]
        )

        # insert_timeseries(
        #     f"extruder_{extruder_id}_component_{component}_lookup_key",
        #     comp["material_index"]
        # )

        insert_timeseries(
            f"extruder_{extruder_id}_component_{component}_set_pct",
            comp["set_pct"]
        )

        insert_timeseries(
            f"extruder_{extruder_id}_component_{component}_act_pct",
            comp["act_pct"]
        )

        insert_timeseries(
            f"extruder_{extruder_id}_component_{component}_set_kg",
            comp["set_kg"]
        )

        insert_timeseries(
            f"extruder_{extruder_id}_component_{component}_act_kg",
            comp["act_kg"]
        )

        insert_timeseries(
            f"extruder_{extruder_id}_component_{component}_density",
            comp["density"]
        )

        insert_timeseries(
            f"extruder_{extruder_id}_component_{component}_deviation",
            comp["deviation"]
        )

    for temp in data["temperature"]:

        insert_timeseries(
            f"extruder_{extruder_id}_temp_{temp['zone']}",
            temp["act"]
        )

    insert_timeseries(
        f"extruder_{extruder_id}_blender_weight",
        data["blender_weight"]
    )

    insert_timeseries(
        f"extruder_{extruder_id}_mixer_weight",
        data["mixer_weight"]
    )


# =========================================================
# FETCH SERIES
# =========================================================

def fetch_series(tag, limit=30):

    conn = get_db()

    cur = conn.cursor()

    cur.execute("""

        SELECT value

        FROM machine_timeseries

        WHERE tag = ?

        ORDER BY id DESC

        LIMIT ?

    """, (

        tag,
        limit

    ))

    rows = cur.fetchall()

    conn.close()

    return [r["value"] for r in rows[::-1]]


# =========================================================
# FETCH LATEST VALUE
# =========================================================

def fetch_latest_value(tag):

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
# FETCH MACHINE OVERVIEW
# =========================================================

def fetch_machine_overview(limit=1):

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
# FETCH LAYER KPIS
# =========================================================

def fetch_layer_kpis(layer_id):

    return {

        "speed": fetch_latest_value(
            f"layer_{layer_id}_speed"
        ),

        "yield": fetch_latest_value(
            f"layer_{layer_id}_yield"
        ),

        "ampere": fetch_latest_value(
            f"layer_{layer_id}_ampere"
        ),

        "melt_pressure": fetch_latest_value(
            f"layer_{layer_id}_melt_pressure"
        ),

        "melt_temperature": fetch_latest_value(
            f"layer_{layer_id}_melt_temperature"
        )
    }


# =========================================================
# FETCH LAYER TRENDS
# =========================================================

def fetch_layer_trends(layer_id, limit=30):

    return {

        "flow_rate": fetch_series(
            f"layer_{layer_id}_flow_rate",
            limit
        ),

        "yield": fetch_series(
            f"layer_{layer_id}_yield",
            limit
        ),

        "thickness": fetch_series(
            f"layer_{layer_id}_thickness",
            limit
        )
    }


# =========================================================
# FETCH WINDER KPIS
# =========================================================

def fetch_winder_kpis(winder_id):

    return {

        "totalizer": fetch_latest_value(
            f"winder_{winder_id}_totalizer"
        ),

        "number_of_rolls": fetch_latest_value(
            f"winder_{winder_id}_number_of_rolls"
        ),

        "roll_length_live": fetch_latest_value(
            f"winder_{winder_id}_roll_length_live"
        ),

        "roll_diameter_live": fetch_latest_value(
            f"winder_{winder_id}_roll_diameter_live"
        )
    }


# =========================================================
# FETCH WINDER TRENDS
# =========================================================

def fetch_winder_trends(winder_id, limit=30):

    return {

        "roll_length": fetch_series(
            f"winder_{winder_id}_roll_length",
            limit
        ),

        "roll_dia": fetch_series(
            f"winder_{winder_id}_roll_dia",
            limit
        )
    }


# =========================================================
# FETCH EXTRUDER COMPONENTS
# =========================================================

def fetch_extruder_components(extruder_id):

    result = []

    for comp in range(1, 7):

        result.append({

            "component": comp,

            "set_pct": fetch_latest_value(
                f"extruder_{extruder_id}_component_{comp}_set_pct"
            ),

            "act_pct": fetch_latest_value(
                f"extruder_{extruder_id}_component_{comp}_act_pct"
            ),

            "set_kg": fetch_latest_value(
                f"extruder_{extruder_id}_component_{comp}_set_kg"
            ),

            "act_kg": fetch_latest_value(
                f"extruder_{extruder_id}_component_{comp}_act_kg"
            ),

            "density": fetch_latest_value(
                f"extruder_{extruder_id}_component_{comp}_density"
            ),

            "deviation": fetch_latest_value(
                f"extruder_{extruder_id}_component_{comp}_deviation"
            )
        })

    return result


# =========================================================
# FETCH EXTRUDER TEMPERATURES
# =========================================================

def fetch_extruder_temperatures(extruder_id):

    zones = [

        "BZ1",
        "BZ2",
        "BZ3",
        "BZ4",
        "BZ5",
        "SC",
        "ADP",
        "ADP-1"

    ]

    return [

        {

            "zone": zone,

            "act": fetch_latest_value(
                f"extruder_{extruder_id}_temp_{zone}"
            )

        }

        for zone in zones
    ]


# =========================================================
# FETCH EXTRUDER SUMMARY
# =========================================================

def fetch_extruder_summary(extruder_id):

    return {

        "blender_weight": fetch_latest_value(
            f"extruder_{extruder_id}_blender_weight"
        ),

        "mixer_weight": fetch_latest_value(
            f"extruder_{extruder_id}_mixer_weight"
        )
    }

