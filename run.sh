#!/usr/bin/env bash

rm products.db
echo -e "\e[1m\e[32mCrawling/Scraping\e[0m"
python3 scrapFravega.py &
python3 scrapGarbarino.py &
wait
echo -e "\e[1m\e[32mGenerating csv reports...\e[0m"
python3 tvReporting.py
python3 acReporting.py
echo -e "\e[1m\e[32mChecking product quantities...\e[0m"
python3 checkProductQuantity.py
echo -e "\e[1m\e[32mDone!\e[0m"
