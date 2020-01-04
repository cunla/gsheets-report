Google spreadsheet email reporter
=================================
This is used to read data from a google spreadsheet, generate a graph from the spreadsheet,
and send it as an email report.
 
# Installation
* Create a virtualenv for the project, python3 is required
```
virtualenv env -p `which python3`
```
* Activate the virtualenv from the project dir for working in terminal
```
$ source env/bin/activate
```
(Setup the the project interpreter in PyCharm)

* Install the project requirements by running
```
$ pip3 install -r requirements.txt
```
* Create the file `secrets.py`, it should have gmail user and app specific password.
In order to obtain app specific password, go to [accounts.google.com](accounts.google.com)
and under **Security** go to **App passwords**
```python
SMTP_SERVER_USER = "you@gmail.com"
SMTP_SERVER_PASSWORD = "xxx"  # Generate app specific code if you have 2FA
```
alternatively, you can add these to `settings.py`
* Enable google spreadsheet api at [https://developers.google.com/sheets/api/quickstart/python](https://developers.google.com/sheets/api/quickstart/python)
Download the client configuration and save `credentials.json` in the same dir
with the project.

# Usage
Edit `settings.py` to match your required needs
```python
# Import from secrets.py
# SMTP_SERVER_USER = "xxx"
# SMTP_SERVER_PASSWORD = "xxx"

from secrets import *

# Google spreadsheet data
SPREADSHEET_ID = '1jMlzxtYrmd'
SPREADSHEET_RANGE = 'Weight!A:C'

# Number of months to include in the report
NUMBER_OF_MONTHS = 6

# SMTP server settings, username and password are stored in secrets.py
SMTP_SERVER = "smtp.gmail.com"
SMTP_SERVER_PORT = 465

# Report sender name and email address
REPORT_SENDER = ("full name", "a@gmail.com")
# Report email subject
REPORT_SUBJECT = 'Report'
# Report recipient name and email address
REPORT_RECIPIENT = ("b", "b@gmail.com")

# Report template
REPORT_TEMPLATE = 'templates/report.html'
```

Afterwards, run 
```
$ python main.py
```

### Tech
* pandas
* jinja2
* google spreadsheets api

### Development
* You can edit the template being sent under `templates/report.html`

# Next steps
* Beautify graph generated by pandas
* 

# Troubleshooting
### Getting `CERTIFICATE_VERIFY_FAILED` error
Your SSL certificates were not installed as part of python. 
Run `tools/install_certificates.py` to install them.