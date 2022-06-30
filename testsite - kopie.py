from flask import Flask, request 
import requests
import time

app = Flask(__name__)

def current_milli_time():
    return round(time.time() * 1000)

@app.route("/")
def hello_world():
    #return '<a href="https://accounts.google.com/o/oauth2/v2/auth?response_type=code&redirect_uri=http://127.0.0.1:5000/new&scope=https://www.googleapis.com/auth/fitness.activity.read&client_id=172619765597-m3tnl50li7sv3rpkh8521uggrsabrbs8.apps.googleusercontent.com">get my data</a>'
    return '<a href="https://accounts.google.com/o/oauth2/v2/auth?response_type=code&redirect_uri=http://127.0.0.1:5000/new&scope=https://www.googleapis.com/auth/fitness.activity.read&client_id=172619765597-m3tnl50li7sv3rpkh8521uggrsabrbs8.apps.googleusercontent.com">get my data</a>'

@app.route("/new")
def gab():
    code = request.args.get("code")
    get_bear_token = "https://oauth2.googleapis.com/token?code=" + (code) + "&grant_type=authorization_code&client_id=172619765597-m3tnl50li7sv3rpkh8521uggrsabrbs8.apps.googleusercontent.com&client_secret=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&redirect_uri=http://127.0.0.1:5000/new"

    post = requests.post(get_bear_token, {})

    post_data = post.json()
    print(post_data)
    if "access_token" not in post_data:
        return "<h1>error</h1>"
    access_token = post_data["access_token"]
    token_type =  post_data["token_type"]

    data_url = "https://www.googleapis.com/fitness/v1/users/me/dataSources"
    headers = {}
    headers["Accept"] = "application/json"
    headers["Authorization"] = token_type + " " + access_token
    data_request = requests.get(data_url, headers=headers)
    """more_data = requests.post("https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate", headers=headers, json={
        "aggregateBy": [{
            "dataTypeName": "com.google.height",
            "dataSourceId": "raw:com.google.height:com.google.android.apps.fitness:user_input"
        }],
       "bucketByTime": { "durationMillis": 86400000 },
        "startTimeMillis": 1655164860000,
        "endTimeMillis": 1655898872000
        })"""
    more_data = requests.get("https://www.googleapis.com/fitness/v1/users/me/dataSources", headers=headers)
    steps_request = requests.post("https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate", headers=headers, json={

        "aggregateBy": [{

            "dataSourceId":

            "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"

        }],

        "bucketByTime": { "durationMillis": 86400000 },

        "startTimeMillis": current_milli_time()-86400000,

        "endTimeMillis": current_milli_time()  

    })
    



    #user_data = more_data.text

   

    #return user_data
    steps_data = steps_request.json()
    user_data = more_data.json()
    """" use code below to print it in html"""
    step_count = steps_data["bucket"][0]["dataset"][0]["point"][0]["value"][0]["intVal"]
    data = {"user_name": "Niels", "step_count": step_count}
    return '<h1>'+data['user_name']+'</h1><h4>Step Count: '+str(data['step_count'])+'</h4>'

    
    
if __name__ == "__main__":
    
    app.run(debug=True)



    

