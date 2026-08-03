# Clasificador de Prendas con Inteligencia Artificial

Proyecto de Inteligencia Artificial para clasificación automática de imágenes de prendas de vestir.

## Clases

El modelo clasifica imágenes en:

- PANTALON
- PLAYERA
- SUDADERA

## Tecnologías

- Python
- TensorFlow / Keras
- FastAPI
- Docker
- GitHub
- MLflow
- Evidently
- Prometheus
- Grafana

## Arquitectura

El sistema está compuesto por un modelo de clasificación de imágenes expuesto mediante una API REST desarrollada con FastAPI y desplegada mediante Docker.

El sistema incorpora monitoreo mediante Prometheus y Grafana, además de detección de Data Drift mediante Evidently.

## Monitoreo

La métrica principal de Data Drift es:

`model_data_drift_detected`

Valores:

- 0: Sistema normal
- 1: Data Drift detectado

## Ejecución

Para ejecutar la aplicación:

```bash
docker build -t clasificador-prendas .