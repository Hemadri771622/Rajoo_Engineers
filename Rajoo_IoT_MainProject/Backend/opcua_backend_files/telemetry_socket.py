# app/sockets/telemetry_socket.py

from app.extensions import socketio
from app.services.db_service import get_updates
from app.services.opcua_buffers import opcua_trends

NAMESPACE = "/telemetry"


def telemetry_task():
    """
    Single source of SocketIO emissions.
    Reads:
    - DB snapshot (machine overview)
    - OPC UA trend buffers (live charts)
    """

    print("[SOCKET] Telemetry task started")

    while True:
        try:
            payload = get_updates()

            # ===============================
            # ATTACH OPC UA TRENDS
            # ===============================
            payload.update({
                "ibc_temp": {
                    "in": list(opcua_trends["ibc_temp"]["in"]),
                    "out": list(opcua_trends["ibc_temp"]["out"])
                },
                "speed_trend": {
                    "set": list(opcua_trends["line_speed"]["set"]),
                    "actual": list(opcua_trends["line_speed"]["actual"])
                },
                "thickness": {
                    "set": list(opcua_trends["thickness"]["set"]),
                    "actual": list(opcua_trends["thickness"]["actual"])
                }
            })

            socketio.emit("telemetry_update", payload, namespace=NAMESPACE)
            socketio.emit("telemetry_update", payload)

            socketio.sleep(1)

        except Exception as e:
            print("[SOCKET] Error:", e)
            socketio.sleep(2)
