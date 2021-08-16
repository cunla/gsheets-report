#!/bin/sh
cd ~/PycharmProjects/gsheets-report
source env/bin/activate
python add_row_data.py $*
