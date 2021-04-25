import logging
import os
import tempfile
from typing import Tuple

import jinja2
import matplotlib.pyplot as plt
import pandas as pd
import requests

import settings
from emails import EmailSender

handler = logging.StreamHandler()
logger = logging.getLogger()
logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))
logger.addHandler(handler)


def download_xls_file(filename: str) -> None:
    url = 'http://www.boi.org.il/he/DataAndStatistics/Lists/BoiTablesAndGraphs/shcd08_h.xls'
    r = requests.get(url)
    logger.info(f'Writing response to file {filename}')
    with open(filename, 'wb') as f:
        f.write(r.content)


def excel_to_dataframe(filename: str) -> pd.DataFrame:
    df = pd.read_excel(filename, header=None, index_col=0, skiprows=9, usecols='A,H')
    df.dropna(inplace=True)
    return df


def get_latest_val(df: pd.DataFrame) -> float:
    latest_val = df.tail(1).get(7).get(0)
    return latest_val


def dataframe_to_image(df: pd.DataFrame, image_filename: str) -> None:
    plt.figure(figsize=(12, 9))
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    start_date = df.index.min().isoformat()[:10]
    end_date = df.index.max().isoformat()[:10]
    plt.title(f"5 years rate BOI {start_date} - {end_date}", fontsize=22)
    latest_val = get_latest_val(df)
    plt.annotate('%0.2f%%' % latest_val, xy=(1, latest_val), xytext=(0, 0),
                 va='center',
                 xycoords=('axes fraction', 'data'),
                 textcoords='offset points')

    plt.plot(df, lw=2.5, )
    plt.savefig(image_filename, bbox_inches="tight")


def send_email(to: Tuple[str], img_attachment: str, html: str, latest_val:float):
    email_sender = EmailSender(settings.SMTP_SERVER,
                               settings.SMTP_SERVER_PORT,
                               settings.SMTP_SERVER_USER,
                               settings.SMTP_SERVER_PASSWORD)
    email_sender.send_email(settings.REPORT_SENDER,
                            to,
                            f'BOI 5 years rate {latest_val:.2f}%',
                            html,
                            attachments=[img_attachment])


def generate_boi_interest_report():
    tempdir = tempfile.TemporaryDirectory()
    tempfile_xls = os.path.join(tempdir.name, 'tmp.xls')
    download_xls_file(tempfile_xls)
    df = excel_to_dataframe(tempfile_xls)
    tempfile_img = os.path.join(tempdir.name, 'tmp.png')
    dataframe_to_image(df, tempfile_img)
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    html_template = template_env.get_template('templates/boi_interest_report.html')
    latest_val = get_latest_val(df)
    html = html_template.render(
        curr_val=latest_val,
    )
    send_email(settings.REPORT_RECIPIENT, tempfile_img, html, latest_val)
    tempdir.cleanup()


if __name__ == '__main__':
    generate_boi_interest_report()
