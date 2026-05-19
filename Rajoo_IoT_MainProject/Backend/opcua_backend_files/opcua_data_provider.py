# app/services/opcua_data_provider.py

import time
from datetime import datetime
from opcua import Client

from app.services.db_service import init_db, get_db
from app.services.opcua_buffers import opcua_trends


# =========================================================
# OPC UA CONFIG
# =========================================================

OPCUA_URL = "opc.tcp://101.101.101.201:4840"

TAGS = {
    # Machine overview (DB + dashboard)
    "total_set_output": "ns=2;s=Studio.tags.Application.g_gross_output_set",
    "total_actual_output": "ns=2;s=Studio.tags.Application.g_gross_output_act",
    "density": "ns=2;s=Studio.tags.Application.g_ext_a_film_avg_density",
    "gsm": "ns=2;s=Studio.tags.Application.g_total_gsm",
    "lay_flat": "ns=2;s=Studio.tags.Application.g_overall_layflat",

    # Trends
    "thickness_set": "ns=2;s=Studio.tags.Application.g_gross_thickness_set",
    "thickness_actual": "ns=2;s=Studio.tags.Application.g_gross_thickness_act",
    "line_speed_set": "ns=2;s=g_overall_linespeed",
    "line_speed_actual": "ns=2;s=g_tower_nip_auto_speed_set",
    "ibc_in": "ns=2;s=Studio.tags.Application.l_ibc_in_act_amp",
    "ibc_out": "ns=2;s=Studio.tags.Application.l_ibc_out_act_amp",
}


# =========================================================
# OPC UA HELPERS
# =========================================================

def connect_opcua():
    """Create and return OPC UA client"""
    client = Client(OPCUA_URL)
    client.connect()
    print("[OPCUA] Connected to server")
    return client


def read_tag(client, node_id):
    """
    Read OPC UA value WITH quality and timestamp
    """
    node = client.get_node(node_id)
    dv = node.get_data_value()

    return {
        "value": dv.Value.Value,
        "quality": dv.StatusCode.name,
        "timestamp": dv.SourceTimestamp or datetime.utcnow()
    }


# =========================================================
# MAIN OPC UA BACKGROUND TASK
# =========================================================

def opcua_data_task():
    """
    This task:
    - Reads OPC UA
    - Updates in-memory trend buffers
    - Inserts snapshot into DB
    """

    print("[OPCUA] Data task started")

    init_db()
    conn = get_db()
    cur = conn.cursor()

    client = connect_opcua()

    while True:
        try:
            # Read all tags
            data = {k: read_tag(client, v) for k, v in TAGS.items()}
            now = datetime.utcnow().strftime("%H:%M:%S")

            # ===============================
            # UPDATE LIVE TREND BUFFERS
            # ===============================
            opcua_trends["ibc_temp"]["in"].append(
                {"x": now, "y": data["ibc_in"]["value"]}
            )
            opcua_trends["ibc_temp"]["out"].append(
                {"x": now, "y": data["ibc_out"]["value"]}
            )

            opcua_trends["line_speed"]["set"].append(
                {"x": now, "y": data["line_speed_set"]["value"]}
            )
            opcua_trends["line_speed"]["actual"].append(
                {"x": now, "y": data["line_speed_actual"]["value"]}
            )

            opcua_trends["thickness"]["set"].append(
                {"x": now, "y": data["thickness_set"]["value"]}
            )
            opcua_trends["thickness"]["actual"].append(
                {"x": now, "y": data["thickness_actual"]["value"]}
            )

            # ===============================
            # DB SNAPSHOT INSERT
            # ===============================
            cur.execute("""
                INSERT INTO machine_overview (
                    total_set_output,
                    total_actual_output,
                    density,
                    gsm,
                    lay_flat
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                data["total_set_output"]["value"],
                data["total_actual_output"]["value"],
                data["density"]["value"],
                data["gsm"]["value"],
                data["lay_flat"]["value"]
            ))

            conn.commit()

            time.sleep(1)

        except Exception as e:
            print("[OPCUA] Error:", e)
            time.sleep(2)
