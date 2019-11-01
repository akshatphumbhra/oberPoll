# oberPoll

A polling web application for improved classroom interactions.


# Travis CI Build Status

[![Build Status](https://travis-ci.com/akshatphumbhra/oberPoll.svg?branch=master)](https://travis-ci.com/akshatphumbhra/oberPoll)

# Set-up Instructions

1) Clone the repository
<br>
2) cd into it
<br>
3) Create a virtual environment with:

$ py -m venv poll

4) Activate your virtual environment

$ poll\Scripts\activate
This should prepend "(poll)" to the start of the prompt
<br>
5) Install the requirements

$ pip install -r requirements.txt
<br>
6) Set the variable "FLASK_APP" to the name of the app

$ set FLASK_APP=oberPoll.py
<br>
7) Run the app with:

$ flask run
<br>
8) Navigate to the required url in your browser. By default this url is http://127.0.0.1:5000/
