#!/usr/bin/env bash

echo "Starting to scrap"
python3 scrapFravega.py &
python3 scrapGarbarino.py &
wait
echo "Generating cvs reports"
python3 tvReporting.py
python3 acReporting.py
echo "Done"
