from io import BytesIO
import streamlit as st
import numpy as np
import PIL.Image
import tensorflow as tf
import pickle
import numpy as np
import csv
from datetime import date
import pandas as pd
import mysql.connector
from sklearn import preprocessing
import matplotlib.pyplot as plt
from tkinter import *

mydb = mysql.connector.connect(host="localhost",user="root",password="root",database="mydatabase")

tab1, tab2, tab3 = st.tabs(["Crop Recommedations", "Disease Predictions", "Fertilizer Recommendations"])

rf_m = open("../models/crop_rec/rf_model.pkl","rb")
knn_m = open("../models/crop_rec/knn_model.pkl","rb")
svm_m = open("../models/crop_rec/svm_model.pkl","rb")

f_m  = open("../models/f_rec/fertilizer_model.pkl","rb")


rf = pickle.load(rf_m)
knn = pickle.load(knn_m)
svm = pickle.load(svm_m)
f = pickle.load(f_m)

list=['png','jpg','jpeg']

f_df = pd.read_csv("../datasets/Fertilizer_Prediction.csv")
label_encoder = preprocessing.LabelEncoder()
f_df['Soil Type']= label_encoder.fit_transform(f_df['Soil Type'])
f_df['Crop Type']= label_encoder.fit_transform(f_df['Crop Type'])

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


    n = st.number_input("N",min_value=0,max_value=300)
    p = st.number_input("P",min_value=0,max_value=300)
    k = st.number_input("K",min_value=0,max_value=300)
    t = st.number_input("Temperature",min_value=0,max_value=100)
    h = st.number_input("Humidity",min_value=0,max_value=100)
    ph = st.number_input("ph levels",min_value=0,max_value=14)
    r = st.number_input("Rainfall",min_value=0,max_value=11872)


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
        image = np.array(PIL.Image.open(BytesIO(file)))
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


            
            #column_name = ["Crop","Disease","Date","Year","Month","Day"]
            data = [crop,c_disease,today,today.year,today.month,today.day]

            with open('../datasets/results.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(data)
                f.close()
        
        graph = pd.read_csv("../datasets/results.csv")
        df = graph.drop(['Disease','Year','Month','Day'],axis=1)

        df_b = df[df['Crop'] == 'Bell Pepper']
        df_p = df[df['Crop'] == 'Potato']
        df_t = df[df['Crop'] == 'Tomato']

        df_filtered_date = df['Date']

        plot_t = df_t.value_counts().sum()
        plot_p = df_p.value_counts().sum()
        plot_b = df_b.value_counts().sum()

        if st.button("Visualize"):
            fig = plt.figure(figsize=(5, 5))
            y = np.array([plot_p,plot_t,plot_b])

            mylabels = ["Potato", "Tomato", "Bell Pepper"]

            plt.pie(y, labels = mylabels, autopct='%1.2f%%')
            st.pyplot(fig)
            
with tab3:
    option_m = st.selectbox('Select desired choice: ',('Disease', 'Overall'))
   
    if option_m == "Disease":
        option_crop = st.selectbox('Select a crop',("Tomato","Potato","Bell Pepper"))

        if option_crop == "Bell Pepper":
            option_dis =  st.selectbox("Select a disease:",("Bacterial spot",""))
        elif option_crop == "Potato":
            option_dis = st.selectbox("Select a disease:",('Early blight','Late blight'))

        elif option_crop == "Tomato":
            option_dis = st.selectbox("Select a disease:",('Bacterial spot','Early blight','Late blight','Leaf Mold','Septoria leaf spot','Spider mites Two spotted spider mite','Target Spot','YellowLeaf Curl Virus','mosaic virus',))

        mycursor = mydb.cursor()

        sql = "SELECT remedy FROM fertilizers WHERE crop = %s AND disease =  %s"
        adr = (option_crop, option_dis, )

        mycursor.execute(sql, adr)

        myresult = mycursor.fetchall()

        if st.button("Show results"):
            st.write("The fertilizers for {} with {} disease are as follows: ".format(option_crop,option_dis))
            for c in  myresult:
                st.write(c[0],"\n")


    elif option_m == "Overall":

            temp1 = st.text_input("Enter Temperature","")
            h1 = st.text_input("Enter Humidity","")
            m1 = st.text_input("Enter Moisture","")
            s1 = st.selectbox("Enter soil type",('Sandy', 'Loamy', 'Black', 'Red', 'Clayey'))
            c1 = st.selectbox("Enter Crop type",('Maize', 'Sugarcane', 'Cotton', 'Tobacco', 'Paddy', 'Barley','Wheat', 'Millets', 'Oil seeds', 'Pulses', 'Ground Nuts'))
            n1 = st.text_input("Enter N","")
            p1 = st.text_input("Enter P","")
            k1 = st.text_input("Enter K","")

            dict1 = {'Sandy':'4', 'Loamy':'2', 'Black':'0', 'Red':'3', 'Clayey':'1'}
            dict2 = {'Maize':'3', 'Sugarcane':'8', 'Cotton':'1', 'Tobacco':'9', 'Paddy':'6', 'Barley':'0',
       'Wheat':'10', 'Millets':'4', 'Oil seeds':'5', 'Pulses':'7', 'Ground Nuts':'2'}
            
            choice_1 = float(dict1["{}".format(s1)])
            print(type(choice_1))
            choice_2 = float(dict2["{}".format(c1)])

            if st.button("Display Predictions"):
                custom = np.array([[temp1,h1,m1,choice_1,choice_2,n1,p1,k1]])
                results_1 = f.predict(custom)
                

                for final in results_1:
                    st.write(final)