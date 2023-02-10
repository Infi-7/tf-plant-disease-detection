from io import BytesIO
import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

tab1, tab2, tab3 = st.tabs(["Crop Recommedations", "Disease Predictions", "Fertilizer Recommendations"])

list=['png','jpg','jpeg']

MODEL = tf.keras.models.load_model("../models/1")

CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]


with tab1:
   st.header("A cat")
   st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
    file = st.file_uploader('Upload a leaf image', type=list)
    show_file = st.empty()
    if not file:
        show_file.info("Please upload a file of type: " + ", ".join(["csv", "png", "jpg"]))
    
    
    else:
        show_file.image(file)


    def read_file_as_image(data) -> np.ndarray:
        image = np.array(Image.open(BytesIO(data)))
        return image


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

with tab3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

