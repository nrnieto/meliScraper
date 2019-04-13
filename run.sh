#!/usr/bin/env bash

echo "Starting to scrap fravega and garbarino"
time python3 scrapFravega.py &
time python3 scrapGarbarino.py &