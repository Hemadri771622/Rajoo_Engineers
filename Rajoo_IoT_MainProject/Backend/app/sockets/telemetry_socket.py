# # print("LOADED telemetry_socket.py FROM:", __file__)

# # import time
# # import traceback
# # from app.extensions import socketio
# # from app.services.db_service import (
# #     fetch_machine_overview,
# #     fetch_series,
# #     fetch_profile,
# #     fetch_zonewise,
# #     fetch_layer_kpis,
# #     fetch_layer_trends,
# #     fetch_winder_kpis,
# #     fetch_winder_trends,

# #     # 🔥 FRONTEND-READY EXTRUDER HELPERS
# #     fetch_extruder_materials_ui,
# #     fetch_extruder_temperature_ui,
# # )

# # # =========================================================
# # # CONFIG
# # # =========================================================
# # WINDOW_SIZE = 30
# # PROFILE_POINTS = 12
# # MAP_POINTS = 9
# # UPDATE_INTERVAL = 10

# # LAYERS = [1, 2, 3]
# # WINDERS = [1, 2]
# # EXTRUDERS = ["A", "B", "C"]

# # clients_connected = 0

# # # =========================================================
# # # HELPERS
# # # =========================================================
# # def window(series, size=WINDOW_SIZE):
# #     return series[-size:] if len(series) > size else series


# # def latest_snapshot_per_index(rows):
# #     latest = {}
# #     for r in rows:
# #         idx = r.get("x", r.get("index_no"))
# #         val = r.get("y", r.get("value"))
# #         latest[idx] = val
# #     return [{"x": k, "y": v} for k, v in sorted(latest.items())]


# # def compute_thickness_stats(actual, thickness_set, gbr_series):
# #     if not actual:
# #         return {
# #             "set": 0,
# #             "avg": 0,
# #             "min": 0,
# #             "max": 0,
# #             "nominal": 18,
# #             "gbr": 0
# #         }

# #     return {
# #         "set": thickness_set[-1] if thickness_set else 18,
# #         "avg": round(sum(actual) / len(actual), 2),
# #         "min": round(min(actual), 2),
# #         "max": round(max(actual), 2),
# #         "nominal": 18,
# #         "gbr": gbr_series[-1] if gbr_series else 0
# #     }

# # # =========================================================
# # # PAYLOAD BUILDERS
# # # =========================================================
# # def build_layer_payload():
# #     return (
# #         {f"layer{i}": fetch_layer_kpis(i) for i in LAYERS},
# #         {f"layer{i}": fetch_layer_trends(i) for i in LAYERS}
# #     )


# # def build_winder_payload():
# #     return (
# #         {f"winder{i}": fetch_winder_kpis(i) for i in WINDERS},
# #         {f"winder{i}": fetch_winder_trends(i) for i in WINDERS}
# #     )


# # def build_extruder_payload():
# #     """
# #      EXACTLY matches frontend expectations
# #     """
# #     extruders = {}

# #     for ex in EXTRUDERS:
# #         extruders[ex] = {
# #             "materials": fetch_extruder_materials_ui(ex),
# #             "temperature": fetch_extruder_temperature_ui(ex),
# #         }

# #     return extruders

# # # =========================================================
# # # TELEMETRY LOOP
# # # =========================================================
# # def telemetry_task():
# #     print("[SOCKET] Telemetry loop started")

# #     while True:
# #         try:
# #             if clients_connected == 0:
# #                 socketio.sleep(1)
# #                 continue

# #             rows = fetch_machine_overview()
# #             latest = rows[-1] if rows else {}

# #             layer_data, layer_trends = build_layer_payload()
# #             winder_data, winder_trends = build_winder_payload()
# #             extruder_data = build_extruder_payload()

# #             payload = {
# #                 # -------- MACHINE KPIs --------
# #                 "machine_overview": {
# #                     "total_set_output": round(latest.get("total_set_output", 0), 2),
# #                     "total_actual_output": round(latest.get("total_actual_output", 0), 2),
# #                     "density": round(latest.get("density", 0), 2),
# #                     "gsm": round(latest.get("gsm", 0), 2),
# #                     "lay_flat": round(latest.get("lay_flat", 0), 2),
# #                 },

# #                 # -------- SPEED --------
# #                 "speed_trend": {
# #                     "set": window(fetch_series("speed_set")),
# #                     "actual": window(fetch_series("speed_actual")),
# #                 },

# #                 # -------- IBC --------
# #                 "ibc_temp": {
# #                     "in": window(fetch_series("ibc_temp_in")),
# #                     "out": window(fetch_series("ibc_temp_out")),
# #                 },

# #                 # -------- PROFILES --------
# #                 "lip_profile": latest_snapshot_per_index(
# #                     fetch_profile("lip_profile")
# #                 )[:PROFILE_POINTS],

# #                 "map_profile": latest_snapshot_per_index(
# #                     fetch_profile("map_profile")
# #                 )[:MAP_POINTS],

# #                 # -------- DIE TEMP --------
# #                 "die_temp_zones": [
# #                     {
# #                         "zone": f"Z{r['index_no']}",
# #                         "set": 0,
# #                         "actual": round(r["value"], 1),
# #                     }
# #                     for r in fetch_zonewise("die_temp")
# #                     if r["index_no"] is not None and r["index_no"] <= 7
# #                 ],

# #                 # -------- THICKNESS --------
# #                 "thickness": {
# #                     "trend": window(fetch_series("thickness_actual")),
# #                     "stats": compute_thickness_stats(
# #                         window(fetch_series("thickness_actual")),
# #                         fetch_series("thickness_set"),
# #                         fetch_series("gbr_position"),
# #                     ),
# #                 },

# #                 # -------- LAYERS --------
# #                 "layer_data": layer_data,
# #                 "layer_trends": layer_trends,

# #                 # -------- WINDERS --------
# #                 "winder_data": winder_data,
# #                 "winder_trends": winder_trends,

# #                 #  -------- EXTRUDERS --------
# #                 "extruders": extruder_data,
# #             }

# #             socketio.emit("telemetry_update", payload)
# #             socketio.sleep(UPDATE_INTERVAL)

# #         except Exception:
# #             print("[SOCKET] Telemetry error:")
# #             print(traceback.format_exc())
# #             socketio.sleep(2)


# # def telemetry_task():
# #     print("[SOCKET] Telemetry loop started")
# #     last_emit_ts = 0  

# #     while True:
# #         try:
# #             if clients_connected == 0:
# #                 socketio.sleep(1)
# #                 continue

# #             now = time.time()
# #             if now - last_emit_ts < UPDATE_INTERVAL:
# #                 socketio.sleep(0.1)
# #                 continue

# #             last_emit_ts = now  # 🔑 TIME TICK FIX

# #             rows = fetch_machine_overview()
# #             latest = rows[-1] if rows else {}

# #             layer_data, layer_trends = build_layer_payload()
# #             winder_data, winder_trends = build_winder_payload()
# #             extruder_data = build_extruder_payload()

# #             payload = {
# #                 "machine_overview": {
# #                     "total_set_output": round(latest.get("total_set_output", 0), 2),
# #                     "total_actual_output": round(latest.get("total_actual_output", 0), 2),
# #                     "density": round(latest.get("density", 0), 2),
# #                     "gsm": round(latest.get("gsm", 0), 2),
# #                     "lay_flat": round(latest.get("lay_flat", 0), 2),
# #                 },

# #                 "speed_trend": {
# #                     "set": window(fetch_series("speed_set")),
# #                     "actual": window(fetch_series("speed_actual")),
# #                 },

# #                 "ibc_temp": {
# #                     "in": window(fetch_series("ibc_temp_in")),
# #                     "out": window(fetch_series("ibc_temp_out")),
# #                 },

# #                 "lip_profile": latest_snapshot_per_index(
# #                     fetch_profile("lip_profile")
# #                 )[:PROFILE_POINTS],

# #                 "map_profile": latest_snapshot_per_index(
# #                     fetch_profile("map_profile")
# #                 )[:MAP_POINTS],

# #                 "die_temp_zones": [
# #                     {
# #                         "zone": f"Z{r['index_no']}",
# #                         "set": 0,
# #                         "actual": round(r["value"], 1),
# #                     }
# #                     for r in fetch_zonewise("die_temp")
# #                     if r["index_no"] is not None and r["index_no"] <= 7
# #                 ],

# #                 "thickness": {
# #                     "trend": window(fetch_series("thickness_actual")),
# #                     "stats": compute_thickness_stats(
# #                         window(fetch_series("thickness_actual")),
# #                         fetch_series("thickness_set"),
# #                         fetch_series("gbr_position"),
# #                     ),
# #                 },

# #                 "layer_data": layer_data,
# #                 "layer_trends": layer_trends,
# #                 "winder_data": winder_data,
# #                 "winder_trends": winder_trends,
# #                 "extruders": extruder_data,
# #             }

# #             socketio.emit("telemetry_update", payload)

# #         except Exception:
# #             print("[SOCKET] Telemetry error:")
# #             print(traceback.format_exc())
# #             socketio.sleep(2)

# # # =========================================================
# # # SOCKET EVENTS
# # # =========================================================
# # @socketio.on("connect")
# # def on_connect():
# #     global clients_connected
# #     clients_connected += 1
# #     print("[SOCKET] Client connected | count =", clients_connected)


# # @socketio.on("disconnect")
# # def on_disconnect():
# #     global clients_connected
# #     clients_connected = max(0, clients_connected - 1)
# #     print("[SOCKET] Client disconnected | count =", clients_connected)


# # # =========================================================
# # # START TELEMETRY LOOP (THREADING SAFE – NO EVENTLET)
# # # =========================================================
# # def start_telemetry():
# #     print("[SOCKET] Starting telemetry background task")
# #     socketio.start_background_task(telemetry_task)



# print("LOADED telemetry_socket.py FROM:", __file__)

# import time
# import traceback
# from app.extensions import socketio
# from app.services.db_service import (
#     fetch_machine_overview,
#     fetch_series,
#     fetch_profile,
#     fetch_zonewise,
#     fetch_layer_kpis,
#     fetch_layer_trends,
#     fetch_winder_kpis,
#     fetch_winder_trends,
#     fetch_extruder_materials_ui,
#     fetch_extruder_temperature_ui,

#     # 🔥 MATERIAL UTILISATION
#     fetch_material_utilisation_series,
#     fetch_material_utilisation_grand_total,
# )

# # =========================================================
# # CONFIG
# # =========================================================
# WINDOW_SIZE = 30
# PROFILE_POINTS = 12
# MAP_POINTS = 9
# UPDATE_INTERVAL = 10

# LAYERS = [1, 2, 3]
# WINDERS = [1, 2]
# EXTRUDERS = ["A", "B", "C"]

# clients_connected = 0

# # =========================================================
# # HELPERS
# # =========================================================
# def window(series, size=WINDOW_SIZE):
#     return series[-size:] if len(series) > size else series


# def latest_snapshot_per_index(rows):
#     latest = {}
#     for r in rows:
#         idx = r.get("x", r.get("index_no"))
#         val = r.get("y", r.get("value"))
#         latest[idx] = val
#     return [{"x": k, "y": v} for k, v in sorted(latest.items())]


# def compute_thickness_stats(actual, thickness_set, gbr_series):
#     if not actual:
#         return {
#             "set": 0,
#             "avg": 0,
#             "min": 0,
#             "max": 0,
#             "nominal": 18,
#             "gbr": 0
#         }

#     return {
#         "set": thickness_set[-1] if thickness_set else 18,
#         "avg": round(sum(actual) / len(actual), 2),
#         "min": round(min(actual), 2),
#         "max": round(max(actual), 2),
#         "nominal": 18,
#         "gbr": gbr_series[-1] if gbr_series else 0
#     }

# # =========================================================
# # PAYLOAD BUILDERS
# # =========================================================
# def build_layer_payload():
#     return (
#         {f"layer{i}": fetch_layer_kpis(i) for i in LAYERS},
#         {f"layer{i}": fetch_layer_trends(i) for i in LAYERS}
#     )


# def build_winder_payload():
#     return (
#         {f"winder{i}": fetch_winder_kpis(i) for i in WINDERS},
#         {f"winder{i}": fetch_winder_trends(i) for i in WINDERS}
#     )


# def build_extruder_payload():
#     extruders = {}

#     for ex in EXTRUDERS:
#         extruders[ex] = {
#             "materials": fetch_extruder_materials_ui(ex),
#             "temperature": fetch_extruder_temperature_ui(ex),
#         }

#     return extruders


# # =========================================================
# # 🔥 MATERIAL UTILISATION PAYLOAD
# # =========================================================
# def build_material_utilisation_payload():
#     data = {}

#     for ex in EXTRUDERS:
#         data[ex] = {
#             "materials": fetch_material_utilisation_series(ex),
#             "grand_total": fetch_material_utilisation_grand_total(ex)
#         }

#     return data


# # =========================================================
# # TELEMETRY LOOP (THREAD SAFE)
# # =========================================================
# def telemetry_task():
#     print("[SOCKET] Telemetry loop started")
#     last_emit_ts = 0

#     while True:
#         try:
#             if clients_connected == 0:
#                 socketio.sleep(1)
#                 continue

#             now = time.time()
#             if now - last_emit_ts < UPDATE_INTERVAL:
#                 socketio.sleep(0.1)
#                 continue

#             last_emit_ts = now

#             rows = fetch_machine_overview()
#             latest = rows[-1] if rows else {}

#             layer_data, layer_trends = build_layer_payload()
#             winder_data, winder_trends = build_winder_payload()
#             extruder_data = build_extruder_payload()

#             # 🔥 NEW
#             material_utilisation_data = build_material_utilisation_payload()

#             payload = {

#                 # -------- MACHINE KPIs --------
#                 "machine_overview": {
#                     "total_set_output": round(latest.get("total_set_output", 0), 2),
#                     "total_actual_output": round(latest.get("total_actual_output", 0), 2),
#                     "density": round(latest.get("density", 0), 2),
#                     "gsm": round(latest.get("gsm", 0), 2),
#                     "lay_flat": round(latest.get("lay_flat", 0), 2),
#                 },

#                 # -------- SPEED --------
#                 "speed_trend": {
#                     "set": window(fetch_series("speed_set")),
#                     "actual": window(fetch_series("speed_actual")),
#                 },

#                 # -------- IBC --------
#                 "ibc_temp": {
#                     "in": window(fetch_series("ibc_temp_in")),
#                     "out": window(fetch_series("ibc_temp_out")),
#                 },

#                 # -------- PROFILES --------
#                 "lip_profile": latest_snapshot_per_index(
#                     fetch_profile("lip_profile")
#                 )[:PROFILE_POINTS],

#                 "map_profile": latest_snapshot_per_index(
#                     fetch_profile("map_profile")
#                 )[:MAP_POINTS],

#                 # -------- DIE TEMP --------
#                 "die_temp_zones": [
#                     {
#                         "zone": f"Z{r['index_no']}",
#                         "set": 0,
#                         "actual": round(r["value"], 1),
#                     }
#                     for r in fetch_zonewise("die_temp")
#                     if r["index_no"] is not None and r["index_no"] <= 7
#                 ],

#                 # -------- THICKNESS --------
#                 "thickness": {
#                     "trend": window(fetch_series("thickness_actual")),
#                     "stats": compute_thickness_stats(
#                         window(fetch_series("thickness_actual")),
#                         fetch_series("thickness_set"),
#                         fetch_series("gbr_position"),
#                     ),
#                 },

#                 # -------- LAYERS --------
#                 "layer_data": layer_data,
#                 "layer_trends": layer_trends,

#                 # -------- WINDERS --------
#                 "winder_data": winder_data,
#                 "winder_trends": winder_trends,

#                 # -------- EXTRUDERS --------
#                 "extruders": extruder_data,

#                 # 🔥 -------- MATERIAL UTILISATION --------
#                 "material_utilisation": material_utilisation_data,
#             }

#             socketio.emit("telemetry_update", payload)

#         except Exception:
#             print("[SOCKET] Telemetry error:")
#             print(traceback.format_exc())
#             socketio.sleep(2)


# # =========================================================
# # SOCKET EVENTS
# # =========================================================
# @socketio.on("connect")
# def on_connect():
#     global clients_connected
#     clients_connected += 1
#     print("[SOCKET] Client connected | count =", clients_connected)


# @socketio.on("disconnect")
# def on_disconnect():
#     global clients_connected
#     clients_connected = max(0, clients_connected - 1)
#     print("[SOCKET] Client disconnected | count =", clients_connected)


# # =========================================================
# # START TELEMETRY LOOP
# # =========================================================
# def start_telemetry():
#     print("[SOCKET] Starting telemetry background task")
#     socketio.start_background_task(telemetry_task)




print("LOADED telemetry_socket.py FROM:", __file__)

import time
import traceback
from app.extensions import socketio
from app.services.db_service import (
    fetch_machine_overview,
    fetch_series,
    fetch_profile,
    fetch_zonewise,
    fetch_layer_kpis,
    fetch_layer_trends,
    fetch_winder_kpis,
    fetch_winder_trends,
    fetch_extruder_materials_ui,
    fetch_extruder_temperature_ui,

    # MATERIAL UTILISATION
    fetch_material_utilisation_series,
    fetch_material_utilisation_grand_total,
)

# =========================================================
# CONFIG
# =========================================================
WINDOW_SIZE = 30
PROFILE_POINTS = 12
MAP_POINTS = 9
UPDATE_INTERVAL = 10

LAYERS = [1, 2, 3]
WINDERS = [1, 2]
EXTRUDERS = ["A", "B", "C"]

clients_connected = 0
latest_payload = {}   # 🔥 SNAPSHOT CACHE

# =========================================================
# HELPERS
# =========================================================
def window(series, size=WINDOW_SIZE):
    return series[-size:] if len(series) > size else series


def latest_snapshot_per_index(rows):
    latest = {}
    for r in rows:
        idx = r.get("x", r.get("index_no"))
        val = r.get("y", r.get("value"))
        latest[idx] = val
    return [{"x": k, "y": v} for k, v in sorted(latest.items())]


def compute_thickness_stats(actual, thickness_set, gbr_series):
    if not actual:
        return {
            "set": 0,
            "avg": 0,
            "min": 0,
            "max": 0,
            "nominal": 18,
            "gbr": 0
        }

    return {
        "set": thickness_set[-1] if thickness_set else 18,
        "avg": round(sum(actual) / len(actual), 2),
        "min": round(min(actual), 2),
        "max": round(max(actual), 2),
        "nominal": 18,
        "gbr": gbr_series[-1] if gbr_series else 0
    }

# =========================================================
# PAYLOAD BUILDERS
# =========================================================
def build_layer_payload():
    return (
        {f"layer{i}": fetch_layer_kpis(i) for i in LAYERS},
        {f"layer{i}": fetch_layer_trends(i) for i in LAYERS}
    )


def build_winder_payload():
    return (
        {f"winder{i}": fetch_winder_kpis(i) for i in WINDERS},
        {f"winder{i}": fetch_winder_trends(i) for i in WINDERS}
    )


def build_extruder_payload():
    extruders = {}
    for ex in EXTRUDERS:
        extruders[ex] = {
            "materials": fetch_extruder_materials_ui(ex),
            "temperature": fetch_extruder_temperature_ui(ex),
        }
    return extruders


def build_material_utilisation_payload():
    data = {}
    for ex in EXTRUDERS:
        data[ex] = {
            "materials": fetch_material_utilisation_series(ex),
            "grand_total": fetch_material_utilisation_grand_total(ex)
        }
    return data


# =========================================================
# TELEMETRY LOOP (THREAD SAFE)
# =========================================================
def telemetry_task():
    print("[SOCKET] Telemetry loop started")
    global latest_payload

    last_emit_ts = 0

    while True:
        try:
            if clients_connected == 0:
                socketio.sleep(1)
                continue

            now = time.time()
            if now - last_emit_ts < UPDATE_INTERVAL:
                socketio.sleep(0.1)
                continue

            last_emit_ts = now

            rows = fetch_machine_overview()
            latest = rows[-1] if rows else {}

            layer_data, layer_trends = build_layer_payload()
            winder_data, winder_trends = build_winder_payload()
            extruder_data = build_extruder_payload()
            material_utilisation_data = build_material_utilisation_payload()

            payload = {

                # -------- MACHINE KPIs --------
                "machine_overview": {
                    "total_set_output": round(latest.get("total_set_output", 0), 2),
                    "total_actual_output": round(latest.get("total_actual_output", 0), 2),
                    "density": round(latest.get("density", 0), 2),
                    "gsm": round(latest.get("gsm", 0), 2),
                    "lay_flat": round(latest.get("lay_flat", 0), 2),
                },

                # -------- SPEED --------
                "speed_trend": {
                    "set": window(fetch_series("speed_set")),
                    "actual": window(fetch_series("speed_actual")),
                },

                # -------- IBC --------
                "ibc_temp": {
                    "in": window(fetch_series("ibc_temp_in")),
                    "out": window(fetch_series("ibc_temp_out")),
                },

                # -------- PROFILES --------
                "lip_profile": latest_snapshot_per_index(
                    fetch_profile("lip_profile")
                )[:PROFILE_POINTS],

                "map_profile": latest_snapshot_per_index(
                    fetch_profile("map_profile")
                )[:MAP_POINTS],

                # -------- DIE TEMP --------
                "die_temp_zones": [
                    {
                        "zone": f"Z{r['index_no']}",
                        "set": 0,
                        "actual": round(r["value"], 1),
                    }
                    for r in fetch_zonewise("die_temp")
                    if r["index_no"] is not None and r["index_no"] <= 7
                ],

                # -------- THICKNESS --------
                "thickness": {
                    "trend": window(fetch_series("thickness_actual")),
                    "stats": compute_thickness_stats(
                        window(fetch_series("thickness_actual")),
                        fetch_series("thickness_set"),
                        fetch_series("gbr_position"),
                    ),
                },

                # -------- LAYERS --------
                "layer_data": layer_data,
                "layer_trends": layer_trends,

                # -------- WINDERS --------
                "winder_data": winder_data,
                "winder_trends": winder_trends,

                # -------- EXTRUDERS --------
                "extruders": extruder_data,

                # -------- MATERIAL UTILISATION --------
                "material_utilisation": material_utilisation_data,
            }

            # 🔥 STORE SNAPSHOT
            latest_payload = payload

            socketio.emit("telemetry_update", payload)

        except Exception:
            print("[SOCKET] Telemetry error:")
            print(traceback.format_exc())
            socketio.sleep(2)


# =========================================================
# SOCKET EVENTS
# =========================================================
@socketio.on("connect")
def on_connect():
    global clients_connected, latest_payload

    clients_connected += 1
    print("[SOCKET] Client connected | count =", clients_connected)

    # 🔥 INSTANT SNAPSHOT FIX (NO FIRST LOAD DELAY)
    if latest_payload:
        socketio.emit("telemetry_update", latest_payload)


@socketio.on("disconnect")
def on_disconnect():
    global clients_connected
    clients_connected = max(0, clients_connected - 1)
    print("[SOCKET] Client disconnected | count =", clients_connected)


# =========================================================
# START TELEMETRY LOOP
# =========================================================
def start_telemetry():
    print("[SOCKET] Starting telemetry background task")
    socketio.start_background_task(telemetry_task)