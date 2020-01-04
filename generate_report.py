from datetime import datetime
from io import StringIO

from dateutil.relativedelta import relativedelta

import pandas as pd

import settings


def dataframe_to_image(df: pd.DataFrame, image_filename: str) -> None:
    fig = df.plot.line().get_figure()
    fig.savefig(image_filename)


def generate_report_from_csv(data) -> pd.DataFrame:
    """
    Generates a report of the last NUMBER_OF_MONTHS months of data from the input.
    :param data: either a filename or an actual csv stream.
    :return: DataFrame with data of the last 6 months.
    """
    df = pd.read_csv(data)
    date_from = datetime.now() - relativedelta(months=+settings.NUMBER_OF_MONTHS)
    df.Date = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df = df[df['Date'] >= date_from]
    df.set_index(['Date'], inplace=True)
    return df


def generate_report_from_csv_str(text: str) -> pd.DataFrame:
    data = StringIO(text)
    return generate_report_from_csv(data)


if __name__ == '__main__':
    df = generate_report_from_csv('weight.csv')
    dataframe_to_image(df, 'weight.png')
