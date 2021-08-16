import argparse
import datetime
import logging
import os
import gsheets
import settings

handler = logging.StreamHandler()
logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))
logger.addHandler(handler)
logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)


def add_weight_row(weight: float) -> None:
    date_str = datetime.date.today().isoformat()
    logger.info(f'Add row with weight {weight} for {date_str}')
    gsheets.write_new_row(settings.SPREADSHEET_ID, settings.SPREADSHEET_RANGE, [date_str, weight])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add line to spreadsheet')
    parser.add_argument('weight', help='Weight to add for today')
    args = parser.parse_args()
    add_weight_row(args.weight)
