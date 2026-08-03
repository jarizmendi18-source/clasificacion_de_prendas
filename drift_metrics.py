import pandas as pd
from prometheus_client import Gauge, start_http_server
import time

# ==========================================
# CONFIGURACIÓN
# ==========================================

DRIFT_THRESHOLD = 0.20
PORT = 8001

# ==========================================
# MÉTRICAS PROMETHEUS
# ==========================================

data_drift_metric = Gauge(
    "model_data_drift_detected",
    "Indica si se detectó Data Drift. 0=Normal, 1=Drift"
)

drift_score_metric = Gauge(
    "model_data_drift_score",
    "Porcentaje máximo de diferencia detectado"
)

# ==========================================
# FUNCIÓN DE DETECCIÓN
# ==========================================

def detect_data_drift():

    reference_data = pd.read_csv(
        "reference_data.csv"
    )

    current_data = pd.read_csv(
        "current_data.csv"
    )

    reference_mean = reference_data.mean(
        numeric_only=True
    )

    current_mean = current_data.mean(
        numeric_only=True
    )

    max_drift = 0
    drift_detected = False

    print("\n" + "=" * 60)
    print("MONITOREO DE DATA DRIFT")
    print("=" * 60)

    for column in reference_data.columns:

        reference_value = reference_mean[column]
        current_value = current_mean[column]

        if reference_value == 0:

            difference = 0

        else:

            difference = abs(
                current_value - reference_value
            ) / abs(reference_value)

        print(
            f"{column}: "
            f"{difference:.2%} de diferencia"
        )

        if difference > max_drift:

            max_drift = difference

        if difference > DRIFT_THRESHOLD:

            drift_detected = True

    # ==========================================
    # ACTUALIZAR MÉTRICAS
    # ==========================================

    if drift_detected:

        data_drift_metric.set(1)

        print("\n🚨 DATA DRIFT DETECTADO")

    else:

        data_drift_metric.set(0)

        print("\n✓ SISTEMA NORMAL")

    drift_score_metric.set(
        max_drift * 100
    )

    print(
        f"Drift máximo: "
        f"{max_drift:.2%}"
    )


# ==========================================
# INICIAR SERVIDOR PROMETHEUS
# ==========================================

print("=" * 60)
print("EXPORTADOR DE MÉTRICAS PROMETHEUS")
print("=" * 60)

print(
    f"Servidor iniciado en "
    f"http://localhost:{PORT}/metrics"
)

start_http_server(PORT)

# ==========================================
# MONITOREO CONTINUO
# ==========================================

while True:

    try:

        detect_data_drift()

    except Exception as e:

        print(
            f"Error durante el monitoreo: {e}"
        )

    time.sleep(30)