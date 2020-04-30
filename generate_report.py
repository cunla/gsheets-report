from datetime import datetime
from io import StringIO
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta

import pandas as pd

import settings


def dataframe_to_image(df: pd.DataFrame, image_filename: str) -> None:
    plt.figure(figsize=(12, 9))
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    y_min = int(min(df.min().values * 0.98))
    y_max = int(max(df.max().values * 1.02))
    plt.ylim(y_min, y_max)
    plt.yticks(range(y_min, y_max, 5), fontsize=14)
    start_date = df.index.min().isoformat()[:10]
    end_date = df.index.max().isoformat()[:10]
    plt.title(f"Weight {start_date} - {end_date}", fontsize=22)

    plt.plot(df, lw=2.5, )
    plt.savefig(image_filename, bbox_inches="tight")



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
