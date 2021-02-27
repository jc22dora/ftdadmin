import urllib
import requests
from io import BytesIO 
from bs4 import BeautifulSoup
import re
from zipfile import ZipFile
import os
import ftdadminmod
import math
header = ['SETTLEMENT DATE', 'CUSIP', 'SYMBOL', 'QUANTITY (FAILS)', 'DESCRIPTION', 'PRICE']


def progress_bar(bytesRead, length):
    currprogress = math.floor(100*(bytesRead/length))
    if currprogress % 5 == 0:
        print(currprogress,"percent complete")
        

def get_latest_csv(conn):
    domain = "https://www.sec.gov"
    ftdurl = "https://www.sec.gov/data/foiadocsfailsdatahtm"
    request = requests.get(ftdurl)
    soup = BeautifulSoup(request.content, 'html.parser')
    url_list = soup.find_all('a', href=re.compile("^/files/data/"))
    latest_csv = url_list[0]
    file_name = latest_csv.get('href',None)
    file_url = domain+file_name
    url,header = urllib.request.urlretrieve(file_url,get_path(file_name.split('/')[-1]))

    with ZipFile(url) as my_zip_file:
        for contained_file in my_zip_file.namelist():
            i, ln = 0, my_zip_file.getinfo(contained_file).file_size
            for line in my_zip_file.open(contained_file).readlines():
                i += len(line)
                line=line.decode('ISO-8859-1')
                row = line.split('|')
                ftdadminmod.process(conn, to_dict(row))
                progress_bar(i, ln)

            ftdadminmod.conncommit(conn)
    

def get_path(file_name):
    script_dir = os.path.dirname(__file__) 
    rel_path = "dailyprocess\\"
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path+file_name

def to_dict(row):
    
    if len(row) == 6:
        return {'SETTLEMENT DATE': row[0], 'CUSIP': row[1], 'SYMBOL': row[2], 'QUANTITY (FAILS)': row[3], 'DESCRIPTION': row[4], 'PRICE': row[5]}
    else:
        return {'SETTLEMENT DATE': None, 'CUSIP': None, 'SYMBOL': None, 'QUANTITY (FAILS)': None, 'DESCRIPTION': None, 'PRICE': None}

    





    
    