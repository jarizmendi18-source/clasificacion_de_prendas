from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import json
import io

# Crear la aplicación
app = FastAPI(title="Clasificador de Prendas")
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
# Permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar el modelo
modelo = load_model("modelo/modelo_prendas.keras")

# Cargar las clases
with open("modelo/clases.json", "r", encoding="utf-8") as f:
    clases = json.load(f)

# Si el JSON es un diccionario, obtener la lista de clases
if isinstance(clases, dict):
    clases = list(clases.values())

@app.get("/")
def inicio():
    return {"mensaje": "API del Clasificador de Prendas funcionando"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contenido = await file.read()

    imagen = Image.open(io.BytesIO(contenido)).convert("RGB")
    imagen = imagen.resize((200, 200))

    imagen = np.array(imagen) / 255.0
    imagen = np.expand_dims(imagen, axis=0)

    prediccion = modelo.predict(imagen)

    indice = int(np.argmax(prediccion))
    confianza = float(np.max(prediccion))

    return {
        "clase": clases[indice],
        "confianza": round(confianza * 100, 2)
    }