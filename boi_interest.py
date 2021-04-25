import logging
import os
import tempfile

import matplotlib.pyplot as plt
import pandas as pd
import requests

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


def dataframe_to_image(df: pd.DataFrame, image_filename: str,) -> None:
    plt.figure(figsize=(12, 9))
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    start_date = df.index.min().isoformat()[:10]
    end_date = df.index.max().isoformat()[:10]
    plt.title(f"5 years rate BOI {start_date} - {end_date}", fontsize=22)
    latest_val = df.tail(1).get(7).get(0)
    plt.annotate('%0.2f%%' % latest_val, xy=(1, latest_val), xytext=(0, 0),
                 va='center',
                 xycoords=('axes fraction', 'data'),
                 textcoords='offset points')

    plt.plot(df, lw=2.5, )
    plt.savefig(image_filename, bbox_inches="tight")


if __name__ == '__main__':
    tempdir = tempfile.TemporaryDirectory()
    tempfile = os.path.join(tempdir.name, 'tmp.xls')
    download_xls_file(tempfile)
    df = excel_to_dataframe(tempfile)

    tempdir.cleanup()
