from io import BytesIO
import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import pickle
import numpy as np
import csv
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt



tab1, tab2, tab3 = st.tabs(["Crop Recommedations", "Disease Predictions", "Fertilizer Recommendations"])

rf_m = open("../models/crop_rec/rf_model.pkl","rb")
knn_m = open("../models/crop_rec/knn_model.pkl","rb")
svm_m = open("../models/crop_rec/svm_model.pkl","rb")


rf = pickle.load(rf_m)
knn = pickle.load(knn_m)
svm = pickle.load(svm_m)

list=['png','jpg','jpeg']

MODEL = tf.keras.models.load_model("../models/disease_pred/1")

today = date.today()


CLASS_NAMES = ['Pepper__bell___Bacterial_spot',
 'Pepper__bell___healthy',
 'Potato___Early_blight',
 'Potato___Late_blight',
 'Potato___healthy',
 'Tomato_Bacterial_spot',
 'Tomato_Early_blight',
 'Tomato_Late_blight',
 'Tomato_Leaf_Mold',
 'Tomato_Septoria_leaf_spot',
 'Tomato_Spider_mites_Two_spotted_spider_mite',
 'Tomato__Target_Spot',
 'Tomato__Tomato_YellowLeaf__Curl_Virus',
 'Tomato__Tomato_mosaic_virus',
 'Tomato_healthy']


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
        show_file.info("Please upload a file of type: " + ", ".join(["jpeg", "png", "jpg"]))
    
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

            print(predicted_class)

            if predicted_class == "Pepper__bell___Bacterial_spot":
                crop = "Bell Pepper"
                c_disease = "Bacterial spot"
                    
            elif predicted_class == "Pepper__bell___healthy":
                crop = "Bell Pepper"
                c_disease = "Healthy"
        
            elif predicted_class == 'Potato___Early_blight':
                crop = "Potato"
                c_disease = 'Early Blight'
            elif predicted_class == 'Potato___Late_blight':
                crop = "Potato"
                c_disease = "Late Blight"
            elif predicted_class == 'Potato___healthy':
                crop = "Potato"
                c_disease = "Healthy"
            
            elif predicted_class == 'Tomato_Bacterial_spot':
                crop = "Tomato"
                c_disease = 'Bacterial spot'
            elif predicted_class == 'Tomato_Early_blight':
                crop = "Tomato"
                c_disease = 'Early blight'                
            elif predicted_class == 'Tomato_Late_blight':
                crop = "Tomato"
                c_disease = 'Late blight'
            elif predicted_class == 'Tomato_Leaf_Mold':
                crop = "Tomato"
                c_disease = 'Leaf Mold'
            elif predicted_class == 'Tomato_Septoria_leaf_spot':
                crop = "Tomato"
                c_disease = 'Septoria leaf spot'
            elif predicted_class == 'Tomato_Spider_mites_Two_spotted_spider_mite':
                crop = "Tomato"
                c_disease = 'Spider mites Two spotted spider mite'
            elif predicted_class == 'Tomato__Target_Spot':
                crop = "Tomato"
                c_disease = 'Target Spot'
            elif predicted_class == 'Tomato__Tomato_YellowLeaf__Curl_Virus':
                crop = "Tomato"
                c_disease = 'YellowLeaf Curl Virus'
            elif predicted_class == 'Tomato__Tomato_mosaic_virus':
                crop = "Tomato"
                c_disease = 'Mosaic virus'
            elif predicted_class == 'Tomato_healthy':
                crop = "Tomato"
                c_disease = 'Healthy'

            
            st.write('Crop :',crop)
            st.write('Disease :',c_disease)
            st.write('Accuracy :',("%.0f%%" % (100 * confidence)))


            
            column_name = ["Crop","Disease","Date","Year","Month","Day"]
            data = [crop,c_disease,today,today.year,today.month,today.day]

            with open('../datasets/results.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(data)
                f.close()
        
        graph = pd.read_csv("../datasets/results.csv")
        y_plot = graph["Crop"]
        x_plot = graph["Date"]

        if st.button("Visualize"):
            plot = pd.read_csv("../datasets/results.csv")
            c_plot=plot
            df = c_plot.drop(['Disease','Year','Month','Day'],axis=1)

            df_t = df[df['Crop'] == 'Tomato']
            plot_t = df_t.value_counts().sum()

            df_p = df[df['Crop'] == 'Potato']
            plot_p = df_p.value_counts().sum()

            df_b = df[df['Crop'] == 'Bell Pepper']
            plot_b = df_b.value_counts().sum()

            plt.rcParams.update({'font.size': 4})

            fig, ax = plt.subplots(figsize=(2, 2))
            y = np.array([plot_p,plot_t,plot_b])

            plt.pie(y, autopct='%1.2f%%')
            st.pyplot(fig) 
            
    if __name__ == "__main__":
        main()

with tab3:
   st.header("hello")
   
