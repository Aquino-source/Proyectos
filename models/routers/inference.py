"""Inference module."""

from fastapi import APIRouter
from PIL import Image
import numpy as np
import tensorflow as tf

from utils.image import download_image
from schemas.inference import ImageInput

router = APIRouter(tags=["Inference Endpoints"])

tmp_path = "./assets/"
tmp_filename = "tmp.jpg"
img_input_size = (224, 224)
model_path = "./models/model.keras"
model = tf.keras.models.load_model(model_path)
class_names = ["Cat", "Dog"]


@router.post("/inference")
def infer_cat_dog(body: ImageInput):
    # Extract info from body
    image_url = body.image_url
    user_id = body.user_id
    save_path = tmp_path + tmp_filename

    # Download image from url reference in tmp folder
    downloaded = download_image(image_url, save_path)
    if not downloaded:
        return {"response": "Error downloading image!"}

    # Load image and validate loading
    image = Image.open(save_path)
    if not image:
        return {"response": "Error loading image!"}

    # Prepare image for inference
    prepared_image = image.resize(img_input_size)
    prepared_image = np.array([prepared_image])

    # Perform inference with model
    inference_response = float(model.predict(prepared_image)[0, 0])

    # Prepare results
    class_id = round(inference_response)
    class_name = class_names[class_id]

    # Build response
    response = {
        "response": "Model enpoint working!",
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
