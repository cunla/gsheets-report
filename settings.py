# Import from secrets.py
# SMTP_SERVER_USER = "xxx"
# SMTP_SERVER_PASSWORD = "xxx"

from secrets import *

# Google spreadsheet data
SPREADSHEET_ID = '1fbFXa0zeedpnF0M0gfoZTjgzORU9db8Vj9D6LmGt2ZM'
SPREADSHEET_RANGE = 'Weight!A:C'

# Number of months to include in the report
NUMBER_OF_MONTHS = 6

# SMTP server settings, username and password are stored in secrets.py
SMTP_SERVER = "smtp.gmail.com"
SMTP_SERVER_PORT = 465

# Report sender name and email address
REPORT_SENDER = ("Daniel Moran", "style.daniel@gmail.com")
# Report email subject
REPORT_SUBJECT = 'Report'
# Report recipient name and email address
REPORT_RECIPIENT = ("Daniel Moran", "style.daniel@gmail.com")

# Report template
REPORT_TEMPLATE = 'templates/report.html'
