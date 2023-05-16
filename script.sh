#!/bin/bash

cd ~/lotto-aggregator
# Activate virtual environment
source venv/bin/activate

# Run Python script and redirect output to log file
python3 update_lotto.py >> cron.log 2>&1
