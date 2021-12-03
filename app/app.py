import sys
import os
import glob
import re
import numpy as np
import tensorflow as tf
import pickle
# Keras
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
model1 = pickle.load(open('c.pkl', 'rb'))
model2 = pickle.load(open('fertilizer.pkl', 'rb'))
MODEL_PATH ='my_model.h5'
model = load_model(MODEL_PATH)

@app.route('/')
def home():
    return render_template('home.html')

#crop prediction
@app.route('/submit',methods=['POST','GET'])
def submit():
    value1 = ""
    if request.method == 'POST':
        
        temp = request.form['temp']
        humid = request.form['humid']
        ph = request.form['ph']
        if ph == 'Neutral':
            ph = 0
        elif ph == 'Acid':
            ph = 1
        else:
            ph = 2
        rf = request.form['moisture']
        soil = request.form['sp']
        if soil == 'Black':
            soil = 0
        elif soil == 'Clayey':
            soil = 1
        elif soil == 'Yellow':
            soil = 4
        elif soil == 'Red':
            soil = 3
        else:
            soil = 2
        prediction1 = model1.predict([[temp,humid,ph,rf,soil]])
        value1= "The crop is"+" "+str(prediction1.all())
        return render_template('soil.html',result=value1)


#fertilizer prediction
@app.route('/submit2',methods=['POST','GET'])
def fertilizer():
    value1 = ""
    if request.method == 'POST':
        temp = request.form['temp']
        humid = request.form['humid']
        rf = request.form['moisture']
        soil = request.form['sp']
        if soil == 'Black':
            soil = 0
        elif soil == 'Clayey':
            soil = 1
        elif soil == 'Loamy':
            soil = 2
        elif soil == 'Red':
            soil = 3
        else:
            soil = 4

        crop = request.form['cp']
        if crop == 'Barley':
            crop = 0
        elif crop == 'Cotton':
            crop = 1      
        elif crop == 'Ground Nuts':
            crop = 2
        elif crop == 'Maize':
            crop = 3 
        elif crop == 'Millets':
            crop = 4
        elif crop == 'Oil seeds':
            crop = 5
        elif crop == 'Paddy':
            crop = 6
        elif crop == 'Pulses':
            crop = 7
        elif crop == 'Sugarcane':
            crop = 8
        elif crop == 'Tobacco':
            crop = 9
        else:
            crop = 10 

        prediction2 = model2.predict([[temp,humid,rf,soil,crop]])
        value1= "The fertilizer is"+" "+str(prediction2.all())
        return render_template('soil_type.html',result=value1)


#soil type prediction
def model_predict(img_path, model):
    print(img_path)
    img = image.load_img(img_path, target_size=(220, 220))

    # Preprocessing the image
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    preds = model.predict(x)
    preds=np.argmax(preds, axis=1)
    if preds==0:
        preds="Black Soil"
    elif preds==1:
        preds="Cinder Soil"
    elif preds==2:
        preds="Laterite Soil"
    elif preds==3:
        preds="Peat Soil"
    elif preds==4:
        preds="Yellow Soil"
    return preds


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = "The soil type is"+" "+str(model_predict(file_path, model))

        return render_template('index.html',result=preds)


      
if __name__ == '__main__':
    app.run(debug=True)
