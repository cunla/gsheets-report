import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

SMTP_SERVER_USER = os.getenv('SMTP_SERVER_USER', None)
SMTP_SERVER_PASSWORD = os.getenv('SMTP_SERVER_PASSWORD', None)


# Google spreadsheet data
SPREADSHEET_ID = '1jMlzxtYrmd1DuTHCd2vxE2u_C71-62Lz6f-me7DSbmA'
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
REPORT_TEMPLATE = 'templates/weight_report.html'
