#!/usr/bin/env bash

echo "
to run the scripts individually:

python fraud-pandas-iterrows.py
python fraud-pandas-merge.py
python fraud-pandas-one-liner.py
python fraud-simple.py


to run the profiler: 


python generate-large-data.py # generates two 1GB files (replaces accounts.csv and transactions.csv)
python profiler.py

"