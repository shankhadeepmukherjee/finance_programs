#import modules
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import re
import time
import datetime
import pandas as pd

#initialise the time-frame
start = "01/01/2016 00:00:00"
end = "01/03/2021 00:00:00"

s = str(int(time.mktime(datetime.datetime.strptime(start, "%d/%m/%Y %H:%M:%S").timetuple())))
e = str(int(time.mktime(datetime.datetime.strptime(end, "%d/%m/%Y %H:%M:%S").timetuple())))

#list of stocks to read
stock_list = pd.read_csv('../input/stock_list.csv')

#scrap the website and save into a different csv files

for i in range(len(stock_list)):
    stock_name = stock_list.stock_name[i]
    
    #open the webpage
    url = 'https://in.finance.yahoo.com/quote/'+stock_name+'/history?period1='+s+'&period2='+e+'&interval=1mo&filter=history&frequency=1mo&includeAdjustedClose=true'
    print(url)
    html = urlopen(url)
    
    #read the html code and row items
    soup = bs(html, features="html.parser")
    all_links = soup.find_all('tr')
    
    #read the cell elements, strip unrequired items and write to a file
    list_rows = []

    for j in all_links:
        row = j.findAll('td')
        c1 = re.compile('<.*?>')
        clean = (re.sub(c1, '',str(row)))
        list_rows.append(clean)
        
    df = pd.DataFrame(list_rows)
    df = df[0].str.split(pat=", ", expand=True)
    df[0] = df[0].str.strip('[')
    df[6] = df[6].str.strip(']')
    df.dropna(inplace = True)
    df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

    out_path = '../input/'+stock_name+'.csv'
        
    df.to_csv(out_path, index = False)
