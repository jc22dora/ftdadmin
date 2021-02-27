import os
import sqlite3
import pandas as pd
import mysql.connector
import pandas.io.sql as sql
import logging 

errorbinpath = os.path.dirname(__file__) 
errorbin = sqlite3.connect(os.path.join(errorbinpath,"dailyprocess\\errorbin.db"))
errorbincursor = errorbin.cursor()


logging.basicConfig(filename='errors.log')

class Connection:
    def __init__(self, user=None, password=None):
        if type(user) is str and type(password) is str:
            connection = mysql.connector.connect(user=user, password=password, host ='104.197.120.134', database='ftdwkey')
        else:
            connection = sqlite3.connect("ftdwkey.db")

        self.connection = connection
        self.cursor = connection.cursor()




def insert_row(self,settlementdate, cusip, symbol, quantity, description, price, jdkey):
    if type(self.connection) is mysql.connector.connection.MySQLConnection:
        self.cursor.execute("INSERT IGNORE INTO ftdwkey VALUES (%s,%s,%s,%s,%s,%s,%s)", (settlementdate, cusip, symbol, quantity, description, price, jdkey))

    else:
        self.cursor.execute("INSERT OR IGNORE INTO ftdwkey VALUES (?,?,?,?,?,?,?)", (settlementdate, cusip, symbol, quantity, description, price, jdkey))
 # Not used

# Not used
def parseFile(path):
    filedata = pd.read_csv(path, delimiter=',')
    return filedata

# Not used
def createDB():
    cursor.execute("CREATE TABLE ftd (settlementdate INTEGER, cusip TEXT, symbol TEXT, quantity INTEGER, description TEXT, price REAL)")

# Not used
def insertFile(filedata):
    row, rows = 0, len(filedata)
    while row < rows:
        insertRow(filedata.iloc[row]) 
        row += 1
    connection.commit()

# Not used
def process_row(self, row):
    #row = {'SETTLEMENT DATE': 20210204, 'CUSIP':'112E45', 'SYMBOL':'TSLA', 'QUANTITY (FAILS)':12, 'DESCRIPTION':'RHRH', 'PRICE\r\n':44.55}
    try:
        settlementdate = row['SETTLEMENT DATE']
        cusip = row['CUSIP']
        symbol = row['SYMBOL']
        quantity = row['QUANTITY (FAILS)']
        description = row['DESCRIPTION']
    except:
        logging.error('dict error',exc_info=True)
        return
    try:
        price = row['PRICE\r\n']
    except:
        try:
            price = row['PRICE\n']
        except:
            try:
                price = row['PRICE']
            except:
                logging.error('price error',exc_info=True)
                return
        
    try:
        #settlementdate conditions
        try:
            int(settlementdate)
        except (ValueError, TypeError, AttributeError):
            raise
        else:
            settlementdate = int(settlementdate)
        #cusip conditions
        try:
            str(cusip)
        except (ValueError, TypeError, AttributeError):
            raise
        else:
            cusip = str(cusip)
        #symbol conditions
        try:
            str(symbol)
        except (ValueError, TypeError, AttributeError):
            raise
        else:
            symbol = str(symbol)
        #quantity conditions
        try:
            int(quantity)
        except (ValueError, TypeError, AttributeError):
            raise
        else:
            quantity = int(quantity)
        #description conditions
        try:
            str(description)
        except (ValueError, TypeError, AttributeError):
            raise
        else:
            description = str(description)
        #price conditions
        try:
            price.rstrip()
        except (AttributeError):
            pass

        try:
            float(price)
        except (ValueError, TypeError, AttributeError):
            raise 
        else:
            price = float(price)

    except (ValueError, TypeError, AttributeError):
        errorbincursor.execute("INSERT INTO errorbin VALUES (?,?,?,?,?,?)", (settlementdate, cusip, symbol, quantity, description, price))
    else:
        #insert
        jdkey = symbol+str(settlementdate)
        #cursor.execute("INSERT IGNORE INTO ftdwkey VALUES (%s,%s,%s,%s,%s,%s,%s)", (settlementdate, cusip, symbol, quantity, description, price, jdkey))
        #cursor.execute("INSERT OR IGNORE INTO ftdwkey VALUES (?,?,?,?,?,?,?)", (settlementdate, cusip, symbol, quantity, description, price, jdkey))
        insert_row(self, settlementdate, cusip, symbol, quantity, description, price, jdkey)

def process(self, row):
    try:
        settlementdate, cusip, symbol, quantity, description = process_dict(row)
        price = process_price(row)
        process_types(settlementdate, cusip, symbol, quantity, description, price)
        #insert
        jdkey = symbol+str(settlementdate)
        #cursor.execute("INSERT IGNORE INTO ftdwkey VALUES (%s,%s,%s,%s,%s,%s,%s)", (settlementdate, cusip, symbol, quantity, description, price, jdkey))
        #cursor.execute("INSERT OR IGNORE INTO ftdwkey VALUES (?,?,?,?,?,?,?)", (settlementdate, cusip, symbol, quantity, description, price, jdkey))
        
        insert_row(self, settlementdate, cusip, symbol, quantity, description, price, jdkey)
    except (ValueError, TypeError, AttributeError):
        errorbincursor.execute("INSERT INTO errorbin VALUES (?,?,?,?,?,?)", (settlementdate, cusip, symbol, quantity, description, price))

def process_dict(row):
    try:
        settlementdate = row['SETTLEMENT DATE']
        cusip = row['CUSIP']
        symbol = row['SYMBOL']
        quantity = row['QUANTITY (FAILS)']
        description = row['DESCRIPTION']
        return settlementdate, cusip, symbol, quantity, description
    except:
        logging.error('dict error',exc_info=True)
        raise

def process_price(row):
    price = None
    try:
        price = row['PRICE\r\n']
    except:
        try:
            price = row['PRICE\n']
        except:
            try:
                price = row['PRICE']
            except:
                logging.error('price error',exc_info=True)
                raise

    return price

def process_types(settlementdate, cusip, symbol, quantity, description, price):

    try:
        int(settlementdate)
    except (ValueError, TypeError, AttributeError):
        raise
    else:
        settlementdate = int(settlementdate)
    #cusip conditions
    try:
        str(cusip)
    except (ValueError, TypeError, AttributeError):
        raise
    else:
        cusip = str(cusip)
    #symbol conditions
    try:
        str(symbol)
    except (ValueError, TypeError, AttributeError):
        raise
    else:
        symbol = str(symbol)
    #quantity conditions
    try:
        int(quantity)
    except (ValueError, TypeError, AttributeError):
        raise
    else:
        quantity = int(quantity)
    #description conditions
    try:
        str(description)
    except (ValueError, TypeError, AttributeError):
        raise
    else:
        description = str(description)
    #price conditions
    try:
        price.rstrip()
    except (AttributeError):
        pass

    try:
        float(price)
    except (ValueError, TypeError, AttributeError):
        raise 
    else:
        price = float(price)
        return settlementdate, cusip, symbol, quantity, description, price

def conncommit(conn):
    conn.connection.commit()
    errorbin.commit()
    print('committed')
    add_timestamp(conn)

def add_timestamp(conn):
    conn.cursor.execute("INSERT INTO logs (last_update) VALUES(NOW())")
    conn.connection.commit()
    print('added time stamp')
