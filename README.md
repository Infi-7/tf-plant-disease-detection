# tf-plant-disease-detection

tensorflow based project for disease detection in plants by implementing image processing using leaves(healthy & infected)

dataset link:- https://www.kaggle.com/datasets/emmarex/plantdisease

delete all files except[Potato early blight,  Potato late blight , Potato healthy]
  
dataset goes in Training folder


-----------------------------------------------------------------------------------------------------------------------------------------

required modules cmd:
  pip install tensorflow==2.8.3 fastapi uvicorn python-multipart pillow tensorflow-serving-api==2.8.3 matplotlib numpy

-----------------------------------------------------------------------------------------------------------------------------------------
alternate steps (conda):
1. conda create -n (env name) python=(version)
2. conda activate (env name)
3. pip install ipykernel
4. python -m ipykernel install --user --name (env name) --display-name "(env name)"
5. conda install tensorflow-gpu

-----------------------------------------------------------------------------------------------------------------------------------------


Postman download link:- https://www.postman.com/downloads/
1. open postman
2. create a request(located on right side)
3. Select post in dropdown
4. select body
5. Enter http://localhost:8000/predict in url
6. Press Send button
