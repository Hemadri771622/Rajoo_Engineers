from app import create_app
from app.extensions import socketio
from app.services.db_service import init_db
from app.services.opc_live_provider import opc_data_task
# from app.services.dummy_data_provider import dummy_data_task
from app.services.material_report_service import generate_material_consumption_pdf
from app.services.thickness_profile_report_service import generate_thickness_profile_pdf
from app.services.production_report_service import generate_production_report
# from app.services.email_service import send_all_reports   
from app.sockets.telemetry_socket import start_telemetry

import time

app = create_app()


def report_background_task():
    print("Waiting 2 minutes before first report...")

    socketio.sleep(120)

    print("Material + Thickness + Production Report Background Task Started")

    while True:
        try:
            material_file = None
            thickness_file = None
            production_file = None

            # ================= MATERIAL REPORT =================
            material_file = generate_material_consumption_pdf(duration_minutes=2)

            if material_file:
                print("Material Report Generated:", material_file)
            else:
                print("Not enough material data.")

            # ================= THICKNESS REPORT =================
            thickness_file = generate_thickness_profile_pdf(duration_minutes=2)

            if thickness_file:
                print("Thickness Report Generated:", thickness_file)
            else:
                print("Not enough thickness data.")

            # ================= PRODUCTION REPORT =================
            production_file = generate_production_report(duration_minutes=2)

            if production_file:
                print("Production Report Generated:", production_file)
            else:
                print("Not enough production data.")

            # ================= EMAIL SECTION =================
            # if material_file or thickness_file or production_file:
            #     try:
            #         send_all_reports()
            #         print("Email sent successfully")
            #     except Exception as email_error:
            #         print("Email sending failed:", email_error)

        except Exception as e:
            print("Report Generation Error:", e)

        socketio.sleep(120)

        
if __name__ == "__main__":
    init_db()
    

    # # Start OPC Live Provider 
    socketio.start_background_task(opc_data_task)


    # socketio.start_background_task(dummy_data_task)
    socketio.start_background_task(report_background_task)

    time.sleep(2)

    start_telemetry()
    
    
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False
    )