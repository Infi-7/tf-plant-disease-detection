from io import BytesIO
import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

list=['png','jpg','jpeg']

MODEL = tf.keras.models.load_model("../models/1")

CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

predicted_class = None

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image


file = st.file_uploader('Upload a PNG image', type=list)
show_file = st.empty()
if not file:
    show_file.info("Please upload a file of type: " + ", ".join(["csv", "png", "jpg"]))
show_file.image(file)

def main():
    
    image = read_file_as_image(file.read())
    img_batch = np.expand_dims(image, 0)
    
    predictions = MODEL.predict(img_batch)

    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])

    if st.button('Predict'):
        st.write('Disease :',predicted_class)
        st.write('Accuracy :',("%.0f%%" % (100 * confidence)))

    
if __name__ == "__main__":
    main()