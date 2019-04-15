#!/usr/bin/env bash

echo "Starting to scrap"
python3 scrapFravega.py &
python3 scrapGarbarino.py &
wait
echo "Done"
