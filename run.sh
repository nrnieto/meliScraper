#!/usr/bin/env bash

echo "scraping"
python3 scrapFravega.py &
python3 scrapGarbarino.py &
echo "finished"