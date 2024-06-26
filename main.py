import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
from io import BytesIO
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

# Load the model from a file
model = load_model('model.h5')

@app.get("/")
def root():
    return {"message": "Server is connected"}

@app.post("/classify")
async def classify_image(image: UploadFile = File(...)):
    # Read the uploaded image
    img_data = await image.read()

    # Open the image using PIL
    img = Image.open(BytesIO(img_data))

    # Convert the image to RGB format
    img = img.convert('RGB')

    # Resize the image to 150x150 pixels
    img = img.resize((150, 150))

    # Convert the image to an array
    x = img_to_array(img)

    # Add a batch dimension to the image array
    x = np.expand_dims(x, axis=0)

    # Preprocess the image
    x = x/255.0  # Assuming your model expects pixel values between 0 and 1

    # Classify the image
    predictions = model.predict(x)

    # Determine the class of the uploaded image
    class_labels = ['ROCK', 'PAPER', 'SCISSORS']
    class_id = np.argmax(predictions[0])
    if class_id < len(class_labels):
        return {"class": class_labels[class_id]}
    else:
        return {"class": "UNKNOWN"}
