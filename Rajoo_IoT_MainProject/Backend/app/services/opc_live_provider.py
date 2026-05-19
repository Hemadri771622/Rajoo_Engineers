import time
import traceback
from opcua import Client
from app.extensions import socketio
from app.services.db_service import (
    init_db,
    insert_machine_overview,
    insert_timeseries
)

# =========================================================
# CONFIG
# =========================================================
UPDATE_INTERVAL = 1
WINDOW_SIZE = 30

DIE_ZONES = 7
LIP_POINTS = 12
MAP_POINTS = 9
LAYERS = [1, 2, 3]
WINDERS = [1, 2]
EXTRUDERS = ["A", "B", "C"]

EXTRUDER_MATERIALS = ["F18010", "LD", "F19010", "PPA705", "MLLD"]
EXTRUDER_ZONES = ["BZ-1", "BZ-3", "ADP", "AD1"]

OPC_URL = "opc.tcp://101.101.101.201:4840"
client = None

# =========================================================
# LIVE GRAPH BUFFERS
# =========================================================
buffers = {}

def update_buffer(key, value):
    if key not in buffers:
        buffers[key] = []
    buffers[key].append(value)
    if len(buffers[key]) > WINDOW_SIZE:
        buffers[key].pop(0)
    return buffers[key]

# =========================================================
# OPC CONNECTION
# =========================================================
def connect_opc():
    global client
    while True:
        try:
            client = Client(OPC_URL)
            client.connect()
            print("[OPC] Connected")
            break
        except Exception as e:
            print("[OPC] Connection failed. Retrying...", e)
            time.sleep(5)

def read(tag):
    try:
        return client.get_node(tag).get_value()
    except:
        return 0

# =========================================================
# MAIN LIVE LOOP
# =========================================================

latest_payload = {}

def opc_data_task():

    init_db()
    connect_opc()
    print("OPC LIVE Provider Started")

    while True:
        start_time = time.time()

        try:
            # ================= MACHINE =================
            machine = {
                "total_set_output": read("ns=6;s=::AsGlobalPV:gVisuPara.TotalExtSetOuput"),
                "total_actual_output": read("ns=6;s=::AsGlobalPV:gVisuPara.TotalExtOuput"),
                "density": read("ns=6;s=::AsGlobalPV:gVisuPara.Density"),
                "gsm": read("ns=6;s=::AsGlobalPV:gVisuPara.GSM"),
                "lay_flat": read("ns=6;s=::AsGlobalPV:gVisuPara.LayFlat"),
            }
            insert_machine_overview(machine)

            # ================= SPEED =================
            speed_set = read("ns=6;s=::AsGlobalPV:gVisuPara.SpeedSet")
            speed_actual = read("ns=6;s=::AsGlobalPV:gVisuPara.SpeedAct")

            insert_timeseries("speed_set", speed_set)
            insert_timeseries("speed_actual", speed_actual)

            speed_set_buf = update_buffer("speed_set", speed_set)
            speed_actual_buf = update_buffer("speed_actual", speed_actual)

            # ================= THICKNESS =================
            thickness_set = read("ns=6;s=::AsGlobalPV:gVisuPara.ThickSet")
            thickness_actual = read("ns=6;s=::AsGlobalPV:gVisuPara.ThickAct")
            gbr = read("ns=6;s=::AsGlobalPV:gVisuPara.GBRPos")

            insert_timeseries("thickness_set", thickness_set)
            insert_timeseries("thickness_actual", thickness_actual)
            insert_timeseries("gbr_position", gbr)

            thickness_buf = update_buffer("thickness_actual", thickness_actual)

            # ================= IBC =================
            ibc_in = read("ns=6;s=::AsGlobalPV:gVisuPara.IBCTempIn")
            ibc_out = read("ns=6;s=::AsGlobalPV:gVisuPara.IBCTempOut")

            insert_timeseries("ibc_temp_in", ibc_in)
            insert_timeseries("ibc_temp_out", ibc_out)

            ibc_in_buf = update_buffer("ibc_in", ibc_in)
            ibc_out_buf = update_buffer("ibc_out", ibc_out)

            # ================= DIE TEMPS =================
            die_temp_zones = []
            for z in range(DIE_ZONES):
                value = read(f"ns=6;s=::AsGlobalPV:HEAT[0].Zone[{z}].Act.Temp")
                insert_timeseries("die_temp", value, index_no=z+1)
                die_temp_zones.append({
                    "zone": f"Z{z+1}",
                    "set": 0,
                    "actual": round(value, 1)
                })

            # ================= LAYERS =================
            layer_data = {}
            layer_trends = {}

            for lid in LAYERS:
                speed = read(f"ns=6;s=::AsGlobalPV:Layer[{lid-1}].Speed")
                yield_val = read(f"ns=6;s=::AsGlobalPV:Layer[{lid-1}].Yield")
                ampere = read(f"ns=6;s=::AsGlobalPV:Layer[{lid-1}].Ampere")
                melt_p = read(f"ns=6;s=::AsGlobalPV:Layer[{lid-1}].MeltPressure")
                melt_t = read(f"ns=6;s=::AsGlobalPV:Layer[{lid-1}].MeltTemp")

                insert_timeseries(f"layer_{lid}_speed", speed)
                insert_timeseries(f"layer_{lid}_yield", yield_val)
                insert_timeseries(f"layer_{lid}_ampere", ampere)
                insert_timeseries(f"layer_{lid}_melt_pressure", melt_p)
                insert_timeseries(f"layer_{lid}_melt_temperature", melt_t)

                layer_data[f"layer{lid}"] = {
                    "speed": speed,
                    "yield": yield_val,
                    "ampere": ampere,
                }

                layer_trends[f"layer{lid}"] = {
                    "melt_pressure": update_buffer(f"layer_{lid}_melt_pressure", melt_p),
                    "melt_temperature": update_buffer(f"layer_{lid}_melt_temperature", melt_t),
                }

            # ================= WINDERS =================
            winder_data = {}
            winder_trends = {}

            for wid in WINDERS:
                totalizer = read(f"ns=6;s=::AsGlobalPV:Winder[{wid-1}].Totalizer")
                roll_length = read(f"ns=6;s=::AsGlobalPV:Winder[{wid-1}].RollLength")
                roll_dia = read(f"ns=6;s=::AsGlobalPV:Winder[{wid-1}].RollDia")

                insert_timeseries(f"winder_{wid}_totalizer", totalizer)
                insert_timeseries(f"winder_{wid}_roll_length", roll_length)
                insert_timeseries(f"winder_{wid}_roll_dia", roll_dia)

                winder_data[f"winder{wid}"] = {
                    "totalizer": totalizer
                }

                winder_trends[f"winder{wid}"] = {
                    "roll_length": update_buffer(f"winder_{wid}_roll_length", roll_length),
                    "roll_dia": update_buffer(f"winder_{wid}_roll_dia", roll_dia),
                }

            # ================= EXTRUDERS =================
            extruders = {}

            for ext in EXTRUDERS:
                materials = {}
                temperature = []

                for mat in EXTRUDER_MATERIALS:
                    set_pct = read(f"ns=6;s=::AsGlobalPV:Extruder{ext}.Material[{mat}].SetPct")
                    act_pct = read(f"ns=6;s=::AsGlobalPV:Extruder{ext}.Material[{mat}].ActPct")

                    insert_timeseries(f"extruder_{ext}_material_{mat}_set_pct", set_pct)
                    insert_timeseries(f"extruder_{ext}_material_{mat}_act_pct", act_pct)

                    materials[mat] = {
                        "set": set_pct,
                        "act": act_pct
                    }

                for zone in EXTRUDER_ZONES:
                    act = read(f"ns=6;s=::AsGlobalPV:Extruder{ext}.Temp[{zone}].Act")
                    insert_timeseries(f"extruder_{ext}_temp_{zone}_act", act)

                    temperature.append({
                        "zone": zone,
                        "set": 0,
                        "act": act
                    })

                extruders[ext] = {
                    "materials": materials,
                    "temperature": temperature
                }

            # ================= FINAL PAYLOAD =================
            payload = {
                "machine_overview": machine,
                "speed_trend": {"set": speed_set_buf, "actual": speed_actual_buf},
                "ibc_temp": {"in": ibc_in_buf, "out": ibc_out_buf},
                "thickness": {
                    "trend": thickness_buf,
                    "stats": {
                        "set": thickness_set,
                        "avg": round(sum(thickness_buf)/len(thickness_buf), 2) if thickness_buf else 0,
                        "min": min(thickness_buf) if thickness_buf else 0,
                        "max": max(thickness_buf) if thickness_buf else 0,
                        "nominal": 18,
                        "gbr": gbr,
                    },
                },
                "die_temp_zones": die_temp_zones,
                "layer_data": layer_data,
                "layer_trends": layer_trends,
                "winder_data": winder_data,
                "winder_trends": winder_trends,
                "extruders": extruders,
            }
             

            global latest_payload

            latest_payload = payload
            socketio.emit("telemetry_update", payload)
            print(" FULL Live Sent + DB Updated")

        except Exception:
            print(traceback.format_exc())
            connect_opc()

        elapsed = time.time() - start_time
        time.sleep(max(0, UPDATE_INTERVAL - elapsed))


@socketio.on("connect")
def handle_connect():
    global latest_payload
    if latest_payload:
        socketio.emit("telemetry_update", latest_payload)