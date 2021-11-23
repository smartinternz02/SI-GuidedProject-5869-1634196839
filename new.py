import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "foVf8TEAB7Y2P-gZMtoGVY5b7-e_GaPO11NbYWGqc0-e"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"fields": [['preg','plas','pres','skin','test','mass','pedi','age']], 
                                   "values": [[6,148,72,35,0,33,0.66,50]]}]}

response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/6b9d8468-2748-41b6-b7b9-6e7680a8b277/predictions?version=2021-10-23', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
predictions = response_scoring.json()
print(predictions)
print('Final Prediction Result',predictions['predictions'][0]['values'][0][0])