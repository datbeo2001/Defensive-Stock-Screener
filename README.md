# Defensive-Stock-Screener
Before you get started, please install pandas, finnhub-python, and openpyxl through pip. If you have an Anaconda environment then you don't need to do so.
This is a stock screener that allows people to sort through a list of stocks and filter out undervalued/defensive stocks.
Once the program starts, it will ask for a path to a file that contains the stocks you want to filter through. Please only put in a file path of a csv or xlsx, xlsm file. If you don't have one, feel free to use the All_Stock.csv file included in this project.
Then it will ask where you want to save the resulting file. DO NOT ATTEMPT TO PUT IN A PATH TO A FILE OR YOU WILL BE STUCK IN AN INFINITE LOOP.
The final thing it will ask is the name of the file. YOU CANNOT INCLUDE THE EXTENSION IN THIS INPUT. The default resulting file will have the xlsx extension.
Since this project attempted API calls from Finnhub, it reads from FinnhubAPIkey.txt, which contains an API key. If you want to speed up, go to finnhub.io and get more API keys then put the key on a new line in that txt file.
The runtime of this program depends on how many API keys from Finnhub you have and how many stocks you want to filter through.



If you have any questions, please email me at manhdat07042001@gmail.com
