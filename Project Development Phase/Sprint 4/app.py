from flask import Flask, render_template, request
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "<ENTER_API_HERE>"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__, static_url_path='')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/checkEligibility')
def checkEligibility():
    return render_template('predict_home.html')

@app.route('/predict', methods=['POST'])
def predict():
    greScore = int(request.form['greScore'])
    toeflScore = int(request.form['toeflScore'])
    univRank = int(request.form['univRank'])
    sop = float(request.form['sop'])
    lor = float(request.form['lor'])
    cgpa = float(request.form['cgpa'])
    research = int(request.form['research'])
    array_of_input_fields = ['greScore', 'toeflScore', 'univRank', 'sop', 'lor', 'cgpa', 'research']
    array_of_values_to_be_scored = [greScore, toeflScore, univRank, sop, lor, cgpa, research]
    payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored]}]}
    # response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/9f4939ed-7f21-4881-8ae4-234e7515f65a/predictions?version=2022-10-21', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/60dd81ed-835f-4d06-8530-e93a50f18e0e/predictions?version=2022-11-13', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    predictions=response_scoring.json()
    prediction = predictions['predictions'][0]['values'][0][0]
    accuracy_percent=predictions['predictions'][0]['values'][0][1]
    accuracy=round(accuracy_percent[1]*100,2)
    if prediction:
        return render_template('chance.html',prediction_rate=accuracy)
    else:
        return render_template('noChance.html',prediction_rate=accuracy)


if __name__ == "__main__":
    app.run()