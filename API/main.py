from io import BytesIO
import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import pickle
import numpy as np

tab1, tab2, tab3 = st.tabs(["Crop Recommedations", "Disease Predictions", "Fertilizer Recommendations"])

rf_m = open("../models/rf_model.pkl","rb")
knn_m = open("../models/rf_model.pkl","rb")
svm_m = open("../models/rf_model.pkl","rb")


rf = pickle.load(rf_m)
knn = pickle.load(knn_m)
svm = pickle.load(svm_m)

list=['png','jpg','jpeg']

MODEL = tf.keras.models.load_model("../models/1")

CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]


with tab1:
   
    option = st.selectbox('How would you like to be contacted?',('RF', 'KNN', 'SVM'))
    st.write('You selected:', option)


    n = st.text_input("N","")
    p = st.text_input("P","")
    k = st.text_input("K","")
    t = st.text_input("Temperature","")
    h = st.text_input("Humidity","")
    ph = st.text_input("ph levels","")
    r = st.text_input("Rainfall","")


    results = ""
    if st.button("Submit"):
        if option == "RF":
            custom = np.array([[n,p,k,t,h,ph,r]])
            result = rf.predict(custom)
            st.success("Prediction using Random Forest : {}".format(result[0]))
        elif option == 'KNN':
            custom = np.array([[n,p,k,t,h,ph,r]])
            result = knn.predict(custom)
            st.success("Prediction using KNN : {}".format(result[0]))
        elif  option == 'SVM':
            custom = np.array([[n,p,k,t,h,ph,r]])
            result = svm.predict(custom)
            st.success("Prediction using SVM : {}".format(result[0]))
    else:
        print("invalid input")

with tab2:
    file = st.file_uploader('Upload a leaf image', type=list)
    show_file = st.empty()
    if not file:
        show_file.info("Please upload a file of type: " + ", ".join(["csv", "png", "jpg"]))
    
    
    else:
        show_file.image(file)


    def read_file_as_image(file) -> np.ndarray:
        image = np.array(Image.open(BytesIO(file)))
        return image


    def main():

        if st.button('Predict'):

            image = read_file_as_image(file.read())
            img_batch = np.expand_dims(image, 0)

            predictions = MODEL.predict(img_batch)
            predicted_class = CLASS_NAMES[np.argmax(predictions[0])]

            confidence = np.max(predictions[0])

            st.write('Disease :',predicted_class)
            st.write('Accuracy :',("%.0f%%" % (100 * confidence)))

            
    if __name__ == "__main__":
        main()

with tab3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

