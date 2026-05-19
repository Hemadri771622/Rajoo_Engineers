print("LOADED telemetry_socket.py FROM:", __file__)

import time
import traceback

from app.extensions import socketio

from app.services.db_service import (
    fetch_machine_overview,
    fetch_series,
    fetch_layer_kpis,
    fetch_layer_trends,
    fetch_winder_kpis,
    fetch_winder_trends,
    fetch_extruder_components,
    fetch_extruder_temperatures,
)

# =========================================================
# CONFIG
# =========================================================

UPDATE_INTERVAL = 5

LAYERS = [1, 2, 3]

WINDERS = [1, 2]

EXTRUDERS = ["A", "B", "C"]

clients_connected = 0

latest_payload = {}


# =========================================================
# HELPERS
# =========================================================

def window(series, size=30):

    return series[-size:] if len(series) > size else series


# =========================================================
# BUILD LAYER PAYLOAD
# =========================================================

def build_layer_payload():

    return (

        {

            f"layer{i}": fetch_layer_kpis(i)

            for i in LAYERS
        },

        {

            f"layer{i}": fetch_layer_trends(i)

            for i in LAYERS
        }
    )


# =========================================================
# BUILD WINDER PAYLOAD
# =========================================================

def build_winder_payload():

    return (

        {

            f"winder{i}": fetch_winder_kpis(i)

            for i in WINDERS
        },

        {

            f"winder{i}": fetch_winder_trends(i)

            for i in WINDERS
        }
    )


# =========================================================
# BUILD EXTRUDER PAYLOAD
# =========================================================

def build_extruder_payload():

    extruders = {}

    for ex in EXTRUDERS:

        extruders[ex] = {

            "materials": fetch_extruder_components(ex),

            "temperature": fetch_extruder_temperatures(ex),
        }

    return extruders


# =========================================================
# TELEMETRY LOOP
# =========================================================

def telemetry_task():

    global latest_payload

    print("[SOCKET] Telemetry loop started")

    while True:

        try:

            if clients_connected == 0:

                socketio.sleep(1)

                continue

            rows = fetch_machine_overview()

            latest = rows[-1] if rows else {}

            layer_data, layer_trends = build_layer_payload()

            winder_data, winder_trends = build_winder_payload()

            extruder_data = build_extruder_payload()

            payload = {

                # =============================================
                # MACHINE OVERVIEW
                # =============================================

                "machine_overview": {

                    "total_set_output": latest.get(
                        "total_set_output", 0
                    ),

                    "total_actual_output": latest.get(
                        "total_actual_output", 0
                    ),

                    "density": latest.get(
                        "density", 0
                    ),

                    "gsm": latest.get(
                        "gsm", 0
                    ),

                    "lay_flat": latest.get(
                        "lay_flat", 0
                    ),

                    "valve_position": latest.get(
                        "valve_position", 0
                    ),

                    "set_tower_nip": latest.get(
                        "set_tower_nip", 0
                    ),

                    "actual_tower_nip": latest.get(
                        "actual_tower_nip", 0
                    ),

                    "set_air_ring": latest.get(
                        "set_air_ring", 0
                    ),

                    "actual_air_ring": latest.get(
                        "actual_air_ring", 0
                    ),

                    "set_regeneration": latest.get(
                        "set_regeneration", 0
                    ),

                    "actual_regeneration": latest.get(
                        "actual_regeneration", 0
                    ),

                    "set_reverse_hauloff": latest.get(
                        "set_reverse_hauloff", 0
                    ),

                    "actual_reverse_hauloff": latest.get(
                        "actual_reverse_hauloff", 0
                    ),
                },

                # =============================================
                # SPEED TREND
                # =============================================

                "speed_trend": {

                    "set": window(
                        fetch_series("speed_set")
                    ),

                    "actual": window(
                        fetch_series("speed_actual")
                    ),
                },

                # =============================================
                # THICKNESS
                # =============================================

                "thickness": {

                    "trend": window(
                        fetch_series("thickness_actual")
                    )
                },

                # =============================================
                # IBC
                # =============================================

                "ibc_temp": {

                    "in": window(
                        fetch_series("ibc_in")
                    ),

                    "out": window(
                        fetch_series("ibc_out")
                    ),
                },

                # =============================================
                # LAYERS
                # =============================================

                "layer_data": layer_data,

                "layer_trends": layer_trends,

                # =============================================
                # WINDERS
                # =============================================

                "winder_data": winder_data,

                "winder_trends": winder_trends,

                # =============================================
                # EXTRUDERS
                # =============================================

                "extruders": extruder_data,
            }

            latest_payload = payload

            socketio.emit(
                "telemetry_update",
                payload
            )

            socketio.sleep(UPDATE_INTERVAL)

        except Exception:

            print("[SOCKET] Telemetry error:")

            print(traceback.format_exc())

            socketio.sleep(2)


# =========================================================
# SOCKET EVENTS
# =========================================================

@socketio.on("connect")
def on_connect():

    global clients_connected
    global latest_payload

    clients_connected += 1

    print(

        "[SOCKET] Client connected | count =",

        clients_connected
    )

    if latest_payload:

        socketio.emit(
            "telemetry_update",
            latest_payload
        )


@socketio.on("disconnect")
def on_disconnect():

    global clients_connected

    clients_connected = max(
        0,
        clients_connected - 1
    )

    print(

        "[SOCKET] Client disconnected | count =",

        clients_connected
    )


# =========================================================
# START TELEMETRY
# =========================================================

def start_telemetry():

    print(
        "[SOCKET] Starting telemetry task"
    )

    socketio.start_background_task(
        telemetry_task
    )