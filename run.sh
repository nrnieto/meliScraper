#!/usr/bin/env bash

echo "Starting to scrap fravega and garbarino"
python3 scrapFravega.py &
python3 scrapGarbarino.py &