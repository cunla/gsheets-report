import tempfile
from typing import Tuple

import jinja2
import os

import settings
from emails import EmailSender
from gsheets import read_spreadsheet_as_csv
from generate_report import dataframe_to_image, generate_report_from_csv_str

TEMP_DIR = tempfile.gettempdir()
TMP_FILENAME = os.path.join(TEMP_DIR, 'graph.png')


def send_spreadsheet_report(to: Tuple[str]):
    """
    Read data from google spreadsheet, generate a graph from data and send it as an email
    :param to   Tuple of (receiver name, receiver email)
    :return:
    """
    io_str = read_spreadsheet_as_csv(settings.SPREADSHEET_ID, settings.SPREADSHEET_RANGE)
    df = generate_report_from_csv_str(io_str.getvalue())
    diff = df.iloc[-1] - df.iloc[0]
    dataframe_to_image(df, TMP_FILENAME)

    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    html_template = template_env.get_template(settings.REPORT_TEMPLATE)
    html = html_template.render(
        months=settings.NUMBER_OF_MONTHS,
        difference=diff['Weight']
    )

    email_sender = EmailSender(settings.SMTP_SERVER, settings.SMTP_SERVER_PORT, settings.SMTP_SERVER_USER,
                               settings.SMTP_SERVER_PASSWORD)
    email_sender.send_email(settings.REPORT_SENDER,
                            to,
                            settings.REPORT_SUBJECT,
                            html,
                            attachments=[TMP_FILENAME])

    os.remove(TMP_FILENAME)


if __name__ == '__main__':
    send_spreadsheet_report(settings.REPORT_RECIPIENT)
