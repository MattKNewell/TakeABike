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

# [START home]
@app.route('/')
def home():
    return render_template('index.html')
# [END home]

@app.route('/results', methods=['POST'])
def calculateRoute():
    origin = request.form['origin']
    destination = request.form ['destination']
    return render_template('results.html', origin=origin, destination=destination)


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
