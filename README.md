# lotto-aggregator
A python script serving a Flask API that aggregates total lottery winnings from different lottos worldwide 

## Setup virtual environment and requirements
1. Setup virtual environment `python3 -m venv venv`
2. Enable venv `source venv/bin/activate`
3. Install requirements.txt `pip install -r requirements.txt`

## Setup the Flask API server using PM2
`pm2 start <path-to-location>/lotto-aggregator/script.sh --interpreter= <path-to-location>/lotto-aggregatort/venv/bin/python3`

## Setup script.sh
1. Fix permission `chmod +x <path-to-location>/lotto-aggregator/script.sh`
2. Type `crontab -e`
3. Put at the end of line `0 0 * * * <path-to-location>/lotto-aggregator/script.sh`. Make sure to save it.
4. The script will run every day at 00:00 UTC to update the `total_winnings.json` 



