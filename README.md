# Defensive-Stock-Screener
Before you get started, please install pandas, finnhub-python, and openpyxl through pip.
This is a stock screener that allows people to sort through a list of stocks and filter out undervalued/defensive stocks.
Once the program starts, it will ask where you want to save your result. DO NOT ATTEMPT TO PUT IN A PATH TO A FILE OR YOU WILL BE STUCK IN AN INFINITE LOOP.

Then it will ask if you want to import your own stock list. If the answer is no, the program will get its own stock list from Finnhub and you can move to the next step. If the answer is yes, there will be another prompt that allows you to input a path to your own stock list. Your stock list must be a csv, or xlsx file. If you input a random file, you will be asked to try again.

Finally, you will be asked to give the filtered list a name. PLEASE DON'T INCLUDE THE EXTENSION SINCE THE RESULTING FILE WILL BE AN .XLSX FILE.

Since this project attempted API calls from Finnhub, it reads from FinnhubAPIkey.txt, which contains an API key. If you want to speed up, go to finnhub.io and get more API keys then put the key on a new line in that txt file.
The runtime of this program depends on how many API keys from Finnhub you have and how many stocks you want to filter through.



If you have any questions, please email me at manhdat07042001@gmail.com
