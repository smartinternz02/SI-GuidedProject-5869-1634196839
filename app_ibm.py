from flask import Flask, render_template, request # Flask is a application
# used to run/serve our application
# request is used to access the file which is uploaded by the user in out application
# render_template is used for rendering the html pages
#import pickle # pickle is used for serializing and de-serializing Python object structures

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "foVf8TEAB7Y2P-gZMtoGVY5b7-e_GaPO11NbYWGqc0-e"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line

app=Flask(__name__) # our flask app

@app.route('/') # rendering the html template
def home():
    return render_template('home.html')
@app.route('/predict') # rendering the html template
def index() :
    return render_template("index.html")

@app.route('/data_predict', methods=['POST']) # route for our prediction
def predict():
    preg = request.form['preg'] # requesting for preg data
    plas = request.form['plas'] # requesting for plas data
    pres = request.form['pres'] # requesting for pres data
    skin = request.form['skin'] # requesting for skin data
    test = request.form['test'] # requesting for test data
    mass = request.form['mass'] # requesting for mass data
    pedi = request.form['pedi'] # requesting for pedi data
    age = request.form['age'] # requesting for age data
    
    # coverting data into float format
    data = [[float(preg), float(plas), float(pres), float(skin), float(test), float(mass), float(pedi), float(age)]]
    print(data)
    # loading model which we saved
    #model = pickle.load(open('Diabeti_Mellitus_Prediction.pkl', 'rb'))
    
    payload_scoring = {"input_data": [{"fields": [['preg','plas','pres','skin','test','mass','pedi','age']], 
                                   "values": data}]}

    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/6b9d8468-2748-41b6-b7b9-6e7680a8b277/predictions?version=2021-10-23', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    #print(response_scoring.json())
    predictions = response_scoring.json()
    print(predictions)
    #print('Final Prediction Result',predictions['predictions'][0]['values'][0][0])
   
    pred = predictions['predictions'][0]['values'][0][0]
    print(pred)
    #prediction= model.predict(data)[0]
    if (pred == 1):
        return render_template('noChance.html', prediction='You have a Diabetic problem, You must and should consult a doctor. Take care')
    else:
        return render_template('chance.html', prediction='You dont have a Diabetic problem')

if __name__ == '__main__':
    app.run()