

from app import create_app
from app.extensions import socketio
from app.services.db_service import init_db

# 🔁 REPLACED: dummy provider → OPC UA provider
from app.services.opcua_data_provider import opcua_data_task

from app.sockets.telemetry_socket import telemetry_task


# =========================================================
# APP BOOTSTRAP
# =========================================================

app = create_app()


if __name__ == "__main__":
    # Ensure DB and tables exist before background tasks start
    init_db()

    # =====================================================
    # BACKGROUND TASKS
    # =====================================================
    # OPC UA data acquisition (PLC → buffers → DB)
    socketio.start_background_task(opcua_data_task)

    # Telemetry emitter (DB + buffers → UI)
    socketio.start_background_task(telemetry_task)

    # =====================================================
    # START SERVER
    # =====================================================
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False  
    )
