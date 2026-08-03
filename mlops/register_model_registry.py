import mlflow
from mlflow import MlflowClient


# ==========================================
# CONFIGURACIÓN
# ==========================================

MLFLOW_URI = "http://127.0.0.1:5000"

EXPERIMENT_NAME = "clasificador-prendas"

MODEL_NAME = "ClasificadorPrendas"


# ==========================================
# CONECTAR CON MLFLOW
# ==========================================

mlflow.set_tracking_uri(MLFLOW_URI)

client = MlflowClient(
    tracking_uri=MLFLOW_URI
)


# ==========================================
# BUSCAR EXPERIMENTO
# ==========================================

experiment = client.get_experiment_by_name(
    EXPERIMENT_NAME
)


if experiment is None:

    raise Exception(
        f"No existe el experimento: {EXPERIMENT_NAME}"
    )


print("=" * 60)

print(
    "REGISTRO EN MODEL REGISTRY"
)

print("=" * 60)

print(
    f"Experimento: {EXPERIMENT_NAME}"
)

print(
    f"ID del experimento: {experiment.experiment_id}"
)


# ==========================================
# BUSCAR RUNS
# ==========================================

runs = client.search_runs(
    experiment_ids=[
        experiment.experiment_id
    ],
    order_by=[
        "start_time DESC"
    ]
)


if len(runs) == 0:

    raise Exception(
        "No existen Runs registrados en el experimento."
    )


# ==========================================
# SELECCIONAR ÚLTIMO RUN
# ==========================================

run = runs[0]

run_id = run.info.run_id

print(
    f"Run seleccionado: {run_id}"
)


# ==========================================
# CONSTRUIR URI DEL MODELO
# ==========================================

model_uri = (
    f"runs:/{run_id}/models/m-"
)


# ==========================================
# MOSTRAR INFORMACIÓN
# ==========================================

print(
    "\nRun encontrado correctamente."
)

print(
    f"Run ID: {run_id}"
)

print(
    f"Estado: {run.info.status}"
)

print(
    "\nEl modelo será gestionado desde MLflow."
)


print("=" * 60)