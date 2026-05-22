import time
import traceback
import pandas as pd

from opcua import Client

from app.extensions import socketio

from app.services.db_service import (

    init_db,

    insert_machine_overview,

    insert_machine_trends,

    insert_ibc_data,

    insert_die_temperatures,

    insert_layer_snapshot,
    insert_layer_trends,

    insert_winder_snapshot,
    insert_winder_trends,

    insert_extruder_snapshot
)

# =========================================================
# CONFIG
# =========================================================

UPDATE_INTERVAL = 1
WINDOW_SIZE = 30

DIE_ZONES = 13
BASE_INDEX = 29

LAYERS = [1, 2, 3]
WINDERS = [1, 2]

# OPC_URL = "opc.tcp://101.101.101.51:48010"
OPC_URL = "opc.tcp://101.101.101.201:4840"

# at home
# ENABLE_OPC = False

#at office(with opc)
ENABLE_OPC = True

client = None

buffers = {}

latest_payload = {}

last_material_reload = 0

# =========================================================
# MATERIAL MASTER
# =========================================================

material_master = {}

material_loaded = False

last_valid_materials = {}

# =========================================================
# LOAD MATERIAL MASTER
# =========================================================

def load_material_master():

    global material_master
    global material_loaded

    try:

        print("===================================")
        print("LOADING MATERIAL MASTER...")
        print("===================================")

        # =================================================
        # READ MATERIAL EXCEL
        # =================================================

        df = pd.read_excel(
            "materials/Materials.xlsx",
            sheet_name="Material_list",
            header=None
        )

        df = df.fillna("")

        # print("===================================")
        # print("MATERIAL EXCEL PREVIEW")
        # print("===================================")

        # print(df.head(20).to_string())

        # print("===================================")

        temp_master = {}

        temp_master = {}

        # =================================================
        # MATERIAL EXCEL STRUCTURE
        #
        # COL 3 = MATERIAL NAME
        # COL 5 = OPC TAG
        # COL 6 = DENSITY
        #
        # OPC TAG FORMAT:
        # g_material_name[1]
        # g_material_name[2]
        # =================================================

        for _, row in df.iterrows():

            try:

                material_name = str(
                    row[3]
                ).strip()

                opc_tag = str(
                    row[5]
                ).strip()

                density = safe_float(
                    row[6]
                )

                # =========================================
                # SKIP EMPTY ROWS
                # =========================================

                if material_name == "":
                    continue

                if opc_tag == "":
                    continue

                # =========================================
                # EXTRACT MATERIAL INDEX
                # FROM:
                # g_material_name[1]
                # TO:
                # 1
                # =========================================

                if "[" not in opc_tag:
                    continue

                try:

                    material_index = int(
                        opc_tag.rsplit("[", 1)[1].split("]")[0]
                    )

                except:
                    continue
                # =========================================
                # STORE IN MASTER
                # =========================================

                temp_master[material_index] = {

                    "material_name": material_name,

                    "density": density
                }

                print(
                    f"LOADED -> "
                    f"INDEX={material_index} | "
                    f"NAME={material_name} | "
                    f"DENSITY={density}"
                )

            except Exception as row_error:

                print(
                    f"ROW SKIPPED -> {row_error}"
                )

        material_master = temp_master

        material_loaded = True

        print("===================================")
        print("MATERIAL MASTER LOADED SUCCESS")
        print(f"TOTAL MATERIALS: {len(material_master)}")
        print("===================================")

    except Exception as e:

        material_loaded = False

        print("===================================")
        print("MATERIAL MASTER LOAD FAILED")
        print(str(e))
        print("===================================")

# =========================================================
# SAFE FLOAT
# =========================================================

def safe_float(v):

    try:

        if v is None:
            return 0

        return float(v)

    except:

        return 0


def update_buffer(key, value):

    global buffers

    if key not in buffers:

        buffers[key] = []

    buffers[key].append(value)

    if len(buffers[key]) > WINDOW_SIZE:

        buffers[key] = buffers[key][-WINDOW_SIZE:]

    return buffers[key]


# =========================================================
# OPC CONNECT
# =========================================================

def connect_opc():

    global client

    while True:

        try:

            if client:

                try:
                    client.disconnect()
                except:
                    pass

            client = Client(OPC_URL)

            client.session_timeout = 30000

            client.connect()

            print("[OPC] Connected")

            break

        except Exception as e:

            print("[OPC] Connection failed:", e)

            time.sleep(5)


# =========================================================
# OPC READ
# =========================================================

def read(tag):

    global client

    try:

        return client.get_node(tag).get_value()

    except Exception as e:

        print(f"OPC READ FAILED -> {tag} -> {e}")

        return 0


# =========================================================
# OPC TASK
# =========================================================

def opc_data_task():

    if not ENABLE_OPC:
        print("[OPC] Disabled")
        return

    global latest_payload
    global last_material_reload

    init_db()

    connect_opc()

    if not material_loaded:

        load_material_master()

    print("===================================")
    print("OPC LIVE Provider Started")
    print("===================================")

    while True:

        try:

            # =================================================
            # PERIODIC MATERIAL RELOAD
            # =================================================

            if time.time() - last_material_reload > 300:

                load_material_master()

                last_material_reload = time.time()

            # =================================================
            # MACHINE OVERVIEW
            # =================================================

            machine = {

                "total_set_output": safe_float(
                    read("ns=2;s=Studio.tags.Application.g_gross_output_set")
                ),

                "total_actual_output": safe_float(
                    read("ns=2;s=Studio.tags.Application.g_gross_output_act")
                ),

                "density": safe_float(
                    read("ns=2;s=Studio.tags.Application.g_ext_a_film_avg_density")
                ),

                "gsm": safe_float(
                    read("ns=2;s=Studio.tags.Application.g_total_gsm")
                ),

                "lay_flat": safe_float(
                    read("ns=2;s=Studio.tags.Application.g_overall_layflat")
                ),

                "valve_position": safe_float(
                    read("ns=2;s=Studio.tags.Application.g_ibc_act_position")
                ),
       

                "set_tower_nip": safe_float(
                    read("ns=2;s=Studio.tags.Application.g_tower_nip_auto_speed_set")
                ),

                "actual_tower_nip": safe_float(
                    read("ns=2;s=Studio.tags.Application.g_overall_linespeed")
                ),

                "set_air_ring": safe_float(
                    read("ns=2;s=Studio.tags.Application.g_obc_set_rpm")
                ),

                "actual_air_ring": safe_float(
                    read("ns=2;s=Studio.tags.Application.g_obc_main_act_rpm")
                ),

                "set_regeneration": safe_float(
                    read("ns=2;s=Studio.tags.Application.g_regeration_blower_set_rpm")
                ),

                "actual_regeneration": safe_float(
                    read("ns=2;s=Studio.tags.Application.g_regeration_blower_act_rpm")
                ),

                "set_reverse_hauloff": safe_float(
                    read("ns=2;s=Studio.tags.Application.g_osc_haul_off_set_rpm")
                ),

                "actual_reverse_hauloff": safe_float(
                    read("ns=2;s=Studio.tags.Application.g_osc_haul_off_act_rpm")
                )
            }

            insert_machine_overview(machine)

            # =================================================
            # LINE SPEED
            # =================================================

            speed_set = safe_float(
                read("ns=2;s=Studio.tags.Application.g_overall_linespeed")
            )

            speed_actual = safe_float(
                read("ns=2;s=Studio.tags.Application.g_tower_nip_auto_speed_set")
            )

            speed_set_buf = update_buffer(
                "speed_set",
                speed_set
            )

            speed_actual_buf = update_buffer(
                "speed_actual",
                speed_actual
            )

            # =================================================
            # THICKNESS
            # =================================================

            thickness_actual = safe_float(
                read("ns=2;s=Studio.tags.Application.g_gross_thickness_act")
            )

            thickness_buf = update_buffer(
                "thickness_actual",
                thickness_actual
            )

            insert_machine_trends(

                speed_set,
                speed_actual,
                thickness_actual
            )

            # =================================================
            # IBC
            # =================================================

            ibc_in = safe_float(
                read("ns=2;s=Studio.tags.Application.l_ibc_in_act_amp")
            )

            ibc_out = safe_float(
                read("ns=2;s=Studio.tags.Application.l_ibc_out_act_amp")
            )

            ibc_in_buf = update_buffer(
                "ibc_in",
                ibc_in
            )

            ibc_out_buf = update_buffer(
                "ibc_out",
                ibc_out
            )

            insert_ibc_data(
                ibc_in,
                ibc_out
            )

            # =================================================
            # DIE TEMPERATURES
            # =================================================

            die_temp_zones = []

            for i in range(DIE_ZONES):

                idx = BASE_INDEX + i

                set_val = safe_float(
                    read(
                        f"ns=2;s=Studio.tags.Application.g_set_temp_{idx}"
                    )
                )

                act_val = safe_float(
                    read(
                        f"ns=2;s=Studio.tags.Application.g_act_temp_{idx}"
                    )
                )

                die_temp_zones.append({

                    "zone": f"Z{i+1}",

                    "set": round(set_val, 2),

                    "actual": round(act_val, 2)
                })

            insert_die_temperatures(
                die_temp_zones
            )

            # =================================================
            # LAYERS
            # =================================================

            layer_data = {}

            layer_trends = {}

            for ext, lid in {

                "a": 1,
                "b": 2,
                "c": 3

            }.items():

                speed = safe_float(
                    read(
                        f"ns=2;s=Studio.tags.Application.g_ext_{ext}_speed_act"
                    )
                )

                yield_val = safe_float(
                    read(
                        f"ns=2;s=Studio.tags.Application.g_ext_{ext}_yield_act"
                    )
                )

                thickness = safe_float(
                    read(
                        f"ns=2;s=Studio.tags.Application.g_ext_{ext}_thickness_act"
                    )
                )

                layer_data[f"layer{lid}"] = {

                    "speed": speed,

                    "yield": yield_val,

                    "ampere": safe_float(
                        read(
                            f"ns=2;s=Studio.tags.Application.g_ext_{ext}_act_amp"
                        )
                    ),

                    "melt_pressure": safe_float(
                        read(
                            f"ns=2;s=Studio.tags.Application.g_melt_pressure_{ext}_act_pre"
                        )
                    ),

                    "melt_temperature": safe_float(
                        read(
                            f"ns=2;s=Studio.tags.Application.g_ext_{ext}_melt_temp"
                        )
                    )
                }

                layer_trends[f"layer{lid}"] = {

                    "flow_rate": update_buffer(
                        f"layer_{lid}_flow_rate",
                        speed
                    ),

                    "yield": update_buffer(
                        f"layer_{lid}_yield",
                        yield_val
                    ),

                    "thickness": update_buffer(
                        f"layer_{lid}_thickness",
                        thickness
                    )
                }

                insert_layer_snapshot(
                    lid,
                    layer_data[f"layer{lid}"]
                )

                insert_layer_trends(
                    lid,
                    layer_trends[f"layer{lid}"]
                )

            # =================================================
            # WINDERS
            # =================================================

            winder_data = {}

            winder_trends = {}

            for wid in WINDERS:

                roll_length = 0

                # roll_length = safe_float(
                #     read(
                #         f"ns=2;s=Studio.tags.Application.g_winder_{wid}_act_roll_length"
                #     )
                # )

                roll_dia = safe_float(
                    read(
                        f"ns=2;s=Studio.tags.Application.g_winder_{wid}_act_roll_dia"
                    )
                )

                totalizer = safe_float(
                    read(
                        f"ns=2;s=Studio.tags.Application.g_winder_{wid}_lenght_totaliser"
                    )
                )

                if totalizer == 0:

                    totalizer = safe_float(
                        read(
                            f"ns=2;s=Studio.tags.Application.g_winder_{wid}_length_totaliser"
                        )
                    )

                try:

                    number_of_rolls = int(
                        float(
                            read(
                                f"ns=2;s=Studio.tags.Application.g_winder_{wid}_no_of_rolls"
                            ) or 0
                        )
                    )

                except Exception:

                    number_of_rolls = 0  


                winder_data[f"winder{wid}"] = {

                    "totalizer": totalizer,

                    "number_of_rolls": number_of_rolls,

                    "roll_length_live": roll_length,

                    "roll_diameter_live": roll_dia
                }

                winder_trends[f"winder{wid}"] = {

                    "roll_length": update_buffer(
                        f"winder_{wid}_roll_length",
                        roll_length
                    ),

                    "roll_dia": update_buffer(
                        f"winder_{wid}_roll_dia",
                        roll_dia
                    )
                }

                insert_winder_snapshot(
                    wid,
                    winder_data[f"winder{wid}"]
                )

                insert_winder_trends(
                    wid,
                    winder_trends[f"winder{wid}"]
                )

            # =================================================
            # EXTRUDERS
            # =================================================

            extruders = {}

            for ext, base in {

                "a": 0,
                "b": 8,
                "c": 16

            }.items():

                components = []

                temps = []

                # =================================================
                # COMPONENTS
                # =================================================

                for i in range(1, 7):

                    # =============================================
                    # MATERIAL INDEX
                    # =============================================

                    try:

                        selection_tag = (
                            f"ns=2;s=Studio.tags.Application."
                            f"g_ext_{ext}_material_select_{i}"
                        )

                        raw_value = read(selection_tag)

                        try:
                            material_index = int(raw_value)
                        except:
                            material_index = 0

                    except Exception as e:

                        print(
                            f"MATERIAL INDEX FAILED EXT={ext} COMP={i} -> {e}"
                        )

                        material_index = 0

                    # =============================================
                    # MATERIAL LOOKUP
                    # =============================================

                    material_name = "NOT SELECTED"
                    density = 0

                    try:

                        material_data = material_master.get(material_index)

                        if material_data:

                            material_name = material_data.get(
                                "material_name",
                                "NOT FOUND"
                            )

                            density = safe_float(
                                material_data.get(
                                    "density",
                                    0
                                )
                            )

                            # =====================================
                            # CACHE LAST VALID MATERIAL
                            # =====================================

                            last_valid_materials[
                                f"{ext}_{i}"
                            ] = {

                                "material_index": material_index,

                                "material_name": material_name,

                                "density": density
                            }

                        else:

                            cache = last_valid_materials.get(
                                f"{ext}_{i}"
                            )

                            if cache:

                                material_index = cache.get(
                                    "material_index",
                                    0
                                )

                                material_name = cache.get(
                                    "material_name",
                                    "NOT FOUND"
                                )

                                density = cache.get(
                                    "density",
                                    0
                                )

                    except Exception as e:

                        print(
                            f"MATERIAL LOOKUP FAILED EXT={ext} COMP={i} -> {e}"
                        )

                    # =============================================
                    # SET %
                    # =============================================

                    try:

                        set_pct = safe_float(
                            read(
                                f"ns=2;s=Studio.tags.Application."
                                f"g_ext_{ext}_set_layer_per_comp_{i}"
                            )
                        )

                    except Exception as e:

                        print(
                            f"SET % FAILED EXT={ext} COMP={i} -> {e}"
                        )

                        set_pct = 0

                    # # =============================================
                    # # ACT %
                    # # =============================================

                    try:

                        act_pct = safe_float(
                            read(
                                f"ns=2;s=Studio.tags.Application."
                                f"g_ext_{ext}_act_layer_per_comp_{i}"
                            )
                        )

                    except Exception as e:

                        print(
                            f"ACT % FAILED EXT={ext} COMP={i} -> {e}"
                        )

                        act_pct = 0

                    # =============================================
                    # SET KG
                    # =============================================

                    try:

                        set_kg = safe_float(
                            read(
                                f"ns=2;s=Studio.tags.Application."
                                f"g_ext_{ext}_set_kg_comp_{i}"
                            )/ 1000
                        )

                    except Exception as e:

                        print(
                            f"SET KG FAILED EXT={ext} COMP={i} -> {e}"
                        )

                        set_kg = 0

                    # =============================================
                    # ACT KG
                    # =============================================

                    try:

                        act_kg = safe_float(
                            read(
                                f"ns=2;s=Studio.tags.Application."
                                f"g_ext_{ext}_act_kg_comp_{i}"
                            )
                        )

                    except Exception as e:

                        print(
                            f"ACT KG FAILED EXT={ext} COMP={i} -> {e}"
                        )

                        act_kg = 0

                    # =============================================
                    # TOTAL KG
                    # =============================================

                    try:

                        total_kg = safe_float(
                            read(
                                f"ns=2;s=Studio.tags.Application."
                                f"g_ext_{ext}_comp_{i}_total_kg"
                            )
                        )

                    except Exception as e:

                        print(
                            f"TOTAL KG FAILED EXT={ext} COMP={i} -> {e}"
                        )

                        total_kg = 0

                    # =============================================
                    # DEVIATION
                    # =============================================

                    deviation = round(
                        set_kg - act_kg,
                        2
                    )

                    # =============================================
                    # FINAL COMPONENT OBJECT
                    # =============================================

                    components.append({

                        "component": i,

                        "material_index": material_index,

                        "material_name": material_name,

                        "density": density,

                        "set_pct": round(set_pct, 2),
                         
                        "act_pct": round(act_pct, 2),

                       
                        "set_kg": round(set_kg, 2),

                        "act_kg": round(act_kg, 2),

                        "total_kg": round(total_kg, 2),

                        

                        "deviation": round(deviation, 2)
                    })

                # =================================================
                # TEMPERATURE ZONES
                # =================================================

                for i, zone in enumerate([

                    "BZ1",
                    "BZ2",
                    "BZ3",
                    "BZ4",
                    "BZ5",
                    "SC",
                    "ADP",
                    "ADP-1"

                ]):

                    idx = base + i

                    # =============================================
                    # SET TEMPERATURE
                    # =============================================

                    try:

                        set_temp = safe_float(
                            read(
                                f"ns=2;s=Studio.tags.Application.g_set_temp_{idx:02d}"
                            )
                        )

                    except Exception as e:

                        print(
                            f"SET TEMP FAILED EXT={ext} ZONE={zone} -> {e}"
                        )

                        set_temp = 0

                    # =============================================
                    # ACTUAL TEMPERATURE
                    # =============================================

                    try:

                        act_temp = safe_float(
                            read(
                                f"ns=2;s=Studio.tags.Application.g_act_temp_{idx:02d}"
                            )
                        )

                    except Exception as e:

                        print(
                            f"ACT TEMP FAILED EXT={ext} ZONE={zone} -> {e}"
                        )

                        act_temp = 0

                    # =============================================
                    # FINAL TEMP OBJECT
                    # =============================================

                    temps.append({

                        "zone": zone,

                        "set": round(set_temp, 2),

                        "act": round(act_temp, 2)
                    })
                # =================================================
                # BLENDER WEIGHT
                # =================================================

                blender_key = f"{ext}_blender_weight"

                try:

                    value = safe_float(
                        read(
                            f"ns=2;s=Studio.tags.Application.g_ext_{ext}_blender_weight"
                        )
                    )

                    if value != 0:
                        last_valid_materials[blender_key] = value

                    blender_weight = last_valid_materials.get(
                        blender_key,
                        0
                    )

                except Exception as e:

                    blender_weight = last_valid_materials.get(
                        blender_key,
                        0
                    )

                # =================================================
                # MIXER WEIGHT
                # =================================================

                mixer_key = f"{ext}_mixer_weight"

                try:

                    value = safe_float(
                        read(
                            f"ns=2;s=Studio.tags.Application.g_ext_{ext}_mixer_weight"
                        )
                    )

                    if value != 0:
                        last_valid_materials[mixer_key] = value

                    mixer_weight = last_valid_materials.get(
                        mixer_key,
                        0
                    )

                except Exception as e:

                    mixer_weight = last_valid_materials.get(
                        mixer_key,
                        0
                    )
                # =================================================
                # FINAL EXTRUDER OBJECT
                # =================================================

                extruders[ext.upper()] = {

                    "components": components,

                    "temperature": temps,

                    "blender_weight": round(blender_weight, 2),

                    "mixer_weight": round(mixer_weight, 2)
                }

                # =================================================
                # DATABASE INSERT
                # =================================================

                try:

                    insert_extruder_snapshot(
                        ext.upper(),
                        extruders[ext.upper()]
                    )

                except Exception as e:

                    print(
                        f"EXTRUDER INSERT FAILED EXT={ext} -> {e}"
                    )                     
                    
            # =================================================
            # FINAL PAYLOAD
            # =================================================

            payload = {

                "heartbeat": int(time.time()),

                "machine_overview": machine,

                "speed_trend": {

                    "set": speed_set_buf,

                    "actual": speed_actual_buf
                },

                "ibc_temp": {

                    "in": ibc_in_buf,

                    "out": ibc_out_buf
                },

                "thickness": {

                    "trend": thickness_buf
                },

                "die_temp_zones": die_temp_zones,

                "layer_data": layer_data,

                "layer_trends": layer_trends,

                "winder_data": winder_data,

                "winder_trends": winder_trends,

                "extruders": extruders
            }

            latest_payload = payload

            try:

                socketio.emit(
                    "telemetry_update",
                    payload
                )

            except Exception as e:

                print("SOCKET EMIT FAILED:", e)

            print("LIVE SENT")

        except Exception:

            print(traceback.format_exc())

            try:

                connect_opc()

            except:
                pass

        time.sleep(UPDATE_INTERVAL)

# =========================================================
# SOCKET CONNECT
# =========================================================

@socketio.on("connect")
def handle_connect():

    global latest_payload

    try:

        if latest_payload:

            socketio.emit(
                "telemetry_update",
                latest_payload
            )

    except Exception as e:

        print("SOCKET CONNECT EMIT FAILED:", e)