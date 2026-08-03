import os
import mlflow
import mlflow.keras
import tensorflow as tf


# ==========================================
# CONFIGURACIÓN
# ==========================================

MODEL_PATH = "modelo/modelo_prendas.keras"

EXPERIMENT_NAME = "clasificador-prendas"

RUN_NAME = "modelo-produccion-v1"


# ==========================================
# VERIFICAR MODELO
# ==========================================

if not os.path.exists(MODEL_PATH):

    raise FileNotFoundError(
        f"No se encontró el modelo: {MODEL_PATH}"
    )


print("=" * 60)
print("REGISTRO DE MODELO EN MLFLOW")
print("=" * 60)


# ==========================================
# CARGAR MODELO KERAS
# ==========================================

print("\nCargando modelo...")

model = tf.keras.models.load_model(
    MODEL_PATH
)

print("Modelo cargado correctamente.")


# ==========================================
# CONFIGURAR EXPERIMENTO
# ==========================================

mlflow.set_experiment(
    EXPERIMENT_NAME
)


# ==========================================
# INICIAR RUN
# ==========================================

with mlflow.start_run(
    run_name=RUN_NAME
):

    # ======================================
    # REGISTRAR PARÁMETROS
    # ======================================

    mlflow.log_param(
        "model_type",
        "TensorFlow Keras"
    )

    mlflow.log_param(
        "model_path",
        MODEL_PATH
    )

    mlflow.log_param(
        "model_version",
        "1.0"
    )

    mlflow.log_param(
        "framework",
        "TensorFlow"
    )


    # ======================================
    # REGISTRAR MODELO
    # ======================================

    print("\nRegistrando modelo en MLflow...")

    mlflow.keras.log_model(
        model,
        name="modelo_prendas"
    )


    print("\n" + "=" * 60)

    print(
        "MODELO REGISTRADO CORRECTAMENTE EN MLFLOW"
    )

    print("=" * 60)

    print(
        f"Experimento: {EXPERIMENT_NAME}"
    )

    print(
        "Versión del modelo: 1.0"
    )

    print(
        "Nombre del artefacto: modelo_prendas"
    )


print("\nProceso finalizado.")