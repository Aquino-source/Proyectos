"""Inference module - Unified version"""

from fastapi import APIRouter, FastAPI
from PIL import Image
import numpy as np
import tensorflow as tf
from pydantic import BaseModel

# Importación externa que subirás después
from utils.image import download_image

# --- SCHEMAS (Integrados) ---
class ImageInput(BaseModel):
    image_url: str
    user_id: str

# --- CONFIGURACIÓN ---
app = FastAPI()
router = APIRouter(tags=["Inference Endpoints"])

TMP_PATH = "./assets/"
TMP_FILENAME = "tmp.jpg"
IMG_INPUT_SIZE = (224, 224)
MODEL_PATH = "./models/model.keras"

# Cargamos el modelo al iniciar (Asegúrate de que la ruta exista)
try:
    model = tf.keras.models.load_model(MODEL_PATH)
except Exception as e:
    print(f"Advertencia: No se pudo cargar el modelo en {MODEL_PATH}. Error: {e}")
    model = None

class_names = ["Cat", "Dog"]

# --- ENDPOINTS ---
@router.post("/inference")
def infer_cat_dog(body: ImageInput):
    # Extract info from body
    image_url = body.image_url
    user_id = body.user_id
    save_path = TMP_PATH + TMP_FILENAME

    # Download image from url reference in tmp folder
    # Nota: Asegúrate de que la carpeta ./assets/ exista localmente
    downloaded = download_image(image_url, save_path)
    if not downloaded:
        return {"response": "Error downloading image!"}

    # Load image and validate loading
    image = Image.open(save_path)
    if not image:
        return {"response": "Error loading image!"}

    # Prepare image for inference
    prepared_image = image.resize(IMG_INPUT_SIZE)
    prepared_image = np.array([prepared_image])

    # Perform inference with model
    if model is None:
        return {"error": "Model not loaded correctly on server"}
        
    inference_response = float(model.predict(prepared_image)[0, 0])

    # Prepare results
    class_id = round(inference_response)
    class_name = class_names[class_id]

    # Build response
    response = {
        "response": "Model endpoint working!",
        "user": user_id,
        "model_response": {
            "model_input_dims": list(prepared_image.shape),
            "inference_response": inference_response,
            "class": class_id,
            "class_name": class_name
        },
        "input_data": {
            "url": image_url,
            "input_dims": list(np.array(image).shape)
        }
    }
    return response

# Incluimos el router en la app de FastAPI
app.include_router(router)
