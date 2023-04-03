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
import mysql.connector
from sklearn import preprocessing

mydb = mysql.connector.connect(host="localhost",user="root",password="root",database="mydatabase")
path = r"C:\Users\infip\OneDrive\Documents\Projects\tf-plant-disease-detection-main\images"
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
   
    n = st.text_input("N","")
    p = st.text_input("P","")
    k = st.text_input("K","")
    t = st.text_input("Temperature","")
    h = st.text_input("Humidity","")
    ph = st.text_input("ph levels","")
    r = st.text_input("Rainfall","")


    if st.button("Submit"):
        custom = np.array([[n,p,k,t,h,ph,r]])
        result = rf.predict(custom)
        st.success(result[0])

        final_dir = path + '\{}.jpg'.format(result[0])
        image = Image.open(final_dir)
        st.image(image, caption='{}'.format(result[0]),width = 400)


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
            chart_data = pd.DataFrame(x_plot,y_plot)

            st.line_chart(chart_data)
            
    if __name__ == "__main__":
        main()

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
                    st.write("The fertilizer recommendations are: ")
                    st.write(final)