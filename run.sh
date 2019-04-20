#!/usr/bin/env bash

echo -e "\e[1m\e[32mStarting to crawl/scrap\e[0m"
python3 scrapFravega.py &
python3 scrapGarbarino.py &
wait
echo -e "\e[1m\e[32mGenerating csv reports...\e[0m"
python3 tvReporting.py
python3 acReporting.py
echo -e "\e[1m\e[32mDone!\e[0m"
