import time
from math import sin
from app.services.db_service import (
    init_db,
    get_db,
    insert_machine_overview,
    insert_timeseries
)

from app.services.report_db_service import (
    init_report_db,
    get_report_db
)

# =========================================================
# CONFIG
# =========================================================
UPDATE_INTERVAL = 10
DIE_ZONES = 7
LIP_POINTS = 12
MAP_POINTS = 9
LAYERS = 3

# =========================================================
# MACHINE STATE
# =========================================================
machine = {
    "total_set_output": 96.0,
    "total_actual_output": 94.0,
    "density": 0.92,
    "gsm": 76.0,
    "lay_flat": 226.0
}

speed_set = 140.0
speed_actual = 138.0
thickness_set = 18.0
gbr_position = 107
tick = 0

# =========================================================
# LAYER STATE
# =========================================================
layers = {
    1: {"thickness_set": 6.0},
    2: {"thickness_set": 6.0},
    3: {"thickness_set": 6.0}
}

# =========================================================
# WINDER STATE
# =========================================================
winders = {
    1: {"roll_length": 250.0, "roll_dia": 600.0},
    2: {"roll_length": 240.0, "roll_dia": 590.0}
}

# =========================================================
# MATERIAL UTILISATION
# =========================================================
MATERIAL_LIST = ["F18010", "LD", "F19010", "PPA705", "MLLD"]

material_utilisation = {
    "A": {mat: 0 for mat in MATERIAL_LIST},
    "B": {mat: 0 for mat in MATERIAL_LIST},
    "C": {mat: 0 for mat in MATERIAL_LIST}
}

# =========================================================
# DUMMY DATA TASK
# =========================================================
def dummy_data_task():
    global tick

    init_db()
    init_report_db()

    print("[DUMMY] Dummy data provider started")

    while True:
        tick += 1

        # =====================================================
        # MACHINE LIVE DATA
        # =====================================================

        machine["total_set_output"] += 1
        machine["total_actual_output"] += 1
        machine["density"] = round(0.92 + sin(tick / 10) * 0.005, 3)
        machine["gsm"] = round(76 + sin(tick / 8), 2)
        machine["lay_flat"] = round(226 + sin(tick / 6) * 2, 2)

        insert_machine_overview(machine)

        current_speed_set = round(speed_set + sin(tick / 5) * 3, 2)
        current_speed_actual = round(speed_actual + sin(tick / 6) * 3, 2)

        insert_timeseries("speed_set", current_speed_set)
        insert_timeseries("speed_actual", current_speed_actual)

        # =====================================================
        # THICKNESS CALCULATION
        # =====================================================

        nominal_thickness = thickness_set
        avg_thickness = round(thickness_set + sin(tick / 7) * 0.6, 2)
        max_thickness = round(avg_thickness + 2.5, 2)
        min_thickness = round(avg_thickness - 2.8, 2)
        control_limit = 5.0
        two_sigma = round(2.8 + sin(tick / 10) * 0.3, 2)

        # =====================================================
        # DATABASE INSERTS
        # =====================================================

        report_conn = get_report_db()
        report_cur = report_conn.cursor()

        # ---------------- PROCESS SUMMARY ----------------
        report_cur.execute("""
            INSERT INTO process_summary (
                nominal_thickness,
                avg_thickness,
                max_thickness,
                min_thickness,
                control_limit,
                two_sigma,
                line_speed,
                gbr_position
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            nominal_thickness,
            avg_thickness,
            max_thickness,
            min_thickness,
            control_limit,
            two_sigma,
            current_speed_actual,
            gbr_position + tick % 5
        ))

        # ---------------- PRODUCTION SUMMARY ----------------
        report_cur.execute("""
            INSERT INTO production_summary (
                total_set_output,
                total_actual_output,
                speed_set,
                speed_actual,
                gsm,
                lay_flat,
                density
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            machine["total_set_output"],
            machine["total_actual_output"],
            current_speed_set,
            current_speed_actual,
            machine["gsm"],
            machine["lay_flat"],
            machine["density"]
        ))

        # ---------------- LAYER SUMMARY ----------------
        for lid, data in layers.items():
            thickness_actual = round(
                data["thickness_set"] + sin((tick + lid) / 6) * 0.25,
                2
            )

            report_cur.execute("""
                INSERT INTO layer_summary (
                    layer_no,
                    thickness_set,
                    thickness_actual
                )
                VALUES (?, ?, ?)
            """, (
                lid,
                data["thickness_set"],
                thickness_actual
            ))

        # ---------------- WINDER SUMMARY ----------------
        for wid, data in winders.items():
            report_cur.execute("""
                INSERT INTO winder_summary (
                    winder_no,
                    roll_length,
                    roll_dia
                )
                VALUES (?, ?, ?)
            """, (
                wid,
                data["roll_length"] + tick,
                data["roll_dia"] + tick
            ))

        # ---------------- MATERIAL UTILISATION ----------------
        for ext_id in material_utilisation:
            for mat in MATERIAL_LIST:
                material_utilisation[ext_id][mat] += 1.0

                report_cur.execute("""
                    INSERT INTO material_utilisation
                    (extruder, material_name, total_kg)
                    VALUES (?, ?, ?)
                """, (
                    ext_id,
                    mat,
                    round(material_utilisation[ext_id][mat], 2)
                ))

        report_conn.commit()
        report_conn.close()

        print("All report data stored successfully")

        # =====================================================
        # EXTRUDER DUMMY DATA (FIXED TAG NAMES)
        # =====================================================

        for ex in ["A", "B", "C"]:

            for mat in MATERIAL_LIST:

                set_kg = round(2.5 + sin(tick / 5) * 0.2, 2)
                act_kg = round(set_kg + sin((tick + 3) / 4) * 0.1, 2)

                set_pct = round(20 + sin(tick / 6) * 2, 2)
                act_pct = round(set_pct + sin((tick + 2) / 5), 2)

                density = round(0.91 + sin(tick / 8) * 0.01, 3)

               # COMPOSITION
                insert_timeseries(
                    f"extruder_{ex}_material_{mat}_set_kg", set_kg
                )
                insert_timeseries(
                    f"extruder_{ex}_material_{mat}_act_kg", act_kg
                )
                insert_timeseries(
                    f"extruder_{ex}_material_{mat}_set_pct", set_pct
                )
                insert_timeseries(
                    f"extruder_{ex}_material_{mat}_act_pct", act_pct
                )
                insert_timeseries(
                    f"extruder_{ex}_material_{mat}_density", density
                )

            # TEMPERATURE
            for zone in ["BZ-1", "BZ-3", "ADP", "AD1"]:

                temp_set = round(90 + sin(tick / 4) * 5, 1)
                temp_act = round(temp_set + sin((tick + 2) / 5) * 3, 1)

                insert_timeseries(
                    f"extruder_{ex}_temp_{zone}_set", temp_set
                )
                insert_timeseries(
                    f"extruder_{ex}_temp_{zone}_act", temp_act
                )

        time.sleep(UPDATE_INTERVAL)