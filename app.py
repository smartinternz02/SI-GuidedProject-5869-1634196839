from flask import Flask, render_template, request # Flask is a application
# used to run/serve our application
# request is used to access the file which is uploaded by the user in out application
# render_template is used for rendering the html pages
import pickle # pickle is used for serializing and de-serializing Python object structures



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
    #print(data)
    # loading model which we saved
    model = pickle.load(open('Diabeti_Mellitus_Prediction.pkl', 'rb'))
    

    prediction= model.predict(data)[0]
    print(prediction)
    if (prediction == 1):
        return render_template('noChance.html', prediction='You have a Diabetic problem, You must and should consult a doctor. Take care')
    else:
        return render_template('chance.html', prediction='You dont have a Diabetic problem')

if __name__ == '__main__':
    app.run()