import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset

from prometheus_client import Gauge, start_http_server

# ==========================================
# CONFIGURACIÓN
# ==========================================

DRIFT_THRESHOLD = 0.20
PROMETHEUS_PORT = 8001

# ==========================================
# MÉTRICA DE PROMETHEUS
# ==========================================

model_data_drift_detected = Gauge(
    "model_data_drift_detected",
    "Indica si se ha detectado Data Drift. 0 = Normal, 1 = Drift detectado"
)

# ==========================================
# INICIAR SERVIDOR DE MÉTRICAS
# ==========================================

start_http_server(PROMETHEUS_PORT)

print("=" * 60)
print("SERVIDOR DE MÉTRICAS PROMETHEUS")
print("=" * 60)
print(f"Métricas disponibles en:")
print(f"http://localhost:{PROMETHEUS_PORT}/metrics")

# ==========================================
# CARGAR DATOS
# ==========================================

reference_data = pd.read_csv("reference_data.csv")
current_data = pd.read_csv("current_data.csv")

print("\n" + "=" * 60)
print("SISTEMA DE MONITOREO DE DATA DRIFT")
print("=" * 60)

# ==========================================
# GENERAR REPORTE EVIDENTLY
# ==========================================

report = Report(
    metrics=[
        DataDriftPreset()
    ]
)

result = report.run(
    reference_data=reference_data,
    current_data=current_data
)

result.save_html("data_drift_report.html")

print("\nReporte Evidently generado correctamente.")

# ==========================================
# ANÁLISIS DE DIFERENCIAS
# ==========================================

reference_mean = reference_data.mean(numeric_only=True)
current_mean = current_data.mean(numeric_only=True)

drift_detected = False

print("\nANÁLISIS DE VARIABLES")
print("-" * 60)

for column in reference_data.columns:

    reference_value = reference_mean[column]
    current_value = current_mean[column]

    # Evitar división entre cero
    if reference_value == 0:
        difference = 0
    else:
        difference = abs(
            current_value - reference_value
        ) / abs(reference_value)

    print(f"\nVariable: {column}")
    print(f"Valor de referencia: {reference_value:.4f}")
    print(f"Valor actual: {current_value:.4f}")
    print(f"Diferencia relativa: {difference:.2%}")

    if difference > DRIFT_THRESHOLD:

        print("⚠️ DRIFT DETECTADO")

        drift_detected = True

    else:

        print("✓ Comportamiento normal")

# ==========================================
# ACTUALIZAR MÉTRICA DE PROMETHEUS
# ==========================================

if drift_detected:

    model_data_drift_detected.set(1)

else:

    model_data_drift_detected.set(0)

# ==========================================
# GENERAR ALERTA
# ==========================================

print("\n" + "=" * 60)

if drift_detected:

    print("🚨 ALERTA: DATA DRIFT DETECTADO")

    print("=" * 60)

    with open("drift_alert.txt", "w", encoding="utf-8") as file:

        file.write("ALERTA DE DATA DRIFT\n")
        file.write("====================\n")
        file.write("Estado: CRÍTICO\n")
        file.write(
            "Se detectaron cambios significativos "
            "en los datos de entrada.\n"
        )
        file.write(
            "Acción recomendada: evaluar el rendimiento "
            "del modelo.\n"
        )
        file.write(
            "Acción posterior: evaluar reentrenamiento.\n"
        )

else:

    print("✓ SISTEMA NORMAL")

    print("=" * 60)

    with open("drift_alert.txt", "w", encoding="utf-8") as file:

        file.write("ESTADO NORMAL\n")
        file.write("====================\n")
        file.write(
            "No se detectó Data Drift significativo.\n"
        )

print("\nProceso de monitoreo finalizado.")

# ==========================================
# MANTENER SERVIDOR ACTIVO
# ==========================================

print("\nServidor de métricas activo.")
print("No cierres esta ventana de PowerShell.")
print(f"Prometheus puede consultar: http://localhost:{PROMETHEUS_PORT}/metrics")

while True:
    pass