# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging

# [START imports]
from flask import Flask, render_template, request
# [END imports]

# [START create_app]
app = Flask(__name__)
# [END create_app]


import requests
import json
import string

def send_request(session, source, destination, api_key, mode):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins="+source+"&mode="+mode+"&destinations="+destination+"&key="+api_key
    req = session.get(url)

    return req

def get_miles(r):
    test_json = json.loads(r.text)['rows']
    return test_json[0]['elements'][0]['distance']['text']

def get_duration(r):
    test_json = json.loads(r.text)['rows']
    return test_json[0]['elements'][0]['duration']['text']



# [START home]
@app.route('/')
def home():
    return render_template('index.html')
# [END home]

@app.route('/results', methods=['POST'])
def calculateRoute():
    origin = request.form['origin']
    destination = request.form ['destination']

    print("origin: " + origin)
    print("destination: " + destination)
    api_k = "AIzaSyCL1hu6LWm9YJqTHOMgqfIt6fUHsPoc4rQ"

    print(requests)
    session = requests.Session()
    req = send_request(session, origin, destination, api_k, "bicycling")
    req1 = send_request(session, origin, destination, api_k, "driving")

    print(get_duration(req))
    print(get_miles(req))
    
    mins_or_hours = get_duration(req).split()[1]
    print(mins_or_hours)
    the_duration = float(get_duration(req).split()[0])
    #the_duration = get_duration(req)
    the_miles = float(get_miles(req).split()[0])

    the_duration_driving = get_duration(req1)
    the_miles_driving = get_miles(req1)

    driving_duration_mins = float(the_duration_driving.split()[0])
    driving_miles = float(the_miles_driving.split()[0])

    the_duration_hrs = the_duration/60
    calories_burned = (the_duration_hrs*600)*2

    gas_saved = (driving_miles/22)*2
    gas_saved = str(round(gas_saved, 2))

    carbon_emissions = 8.8*(driving_miles/22)*2
    carbon_emissions = str(round(carbon_emissions, 2))

    print(driving_duration_mins)
    print(driving_miles)

    return render_template('results.html', origin=origin, destination=destination, 
        the_duration=the_duration, the_miles=the_miles, the_calories=calories_burned, 
        the_gas=gas_saved, the_duration_driving=the_duration_driving, the_miles_driving=the_miles_driving, 
        carbon_emissions=carbon_emissions, mins_or_hours=mins_or_hours)

# [START info]
@app.route('/info')
def info():
    return render_template('info.html')
# [END info]

# [START about]
@app.route('/about')
def about():
    return render_template('about.html')
# [END about]

# [START form]
@app.route('/form')
def form():
    labels = "123"
    return render_template('form.html', labels=labels)
# [END form]



# [START submitted]
@app.route('/submitted', methods=['POST'])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']

    # [END submitted]
    # [START render_template]
    return render_template(
        'submitted_form.html',
        name=name,
        email=email,
        site=site,
        comments=comments)
    # [END render_template]


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080,debug=True)
