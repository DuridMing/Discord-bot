'''
finance csv file operator
'''

from datetime import datetime, timezone, timedelta
import os
import csv
import pandas as pd

import finance.chart as chart
from config import *

# import chart
# DATA_PATH = "data/"

csv_path = DATA_PATH +"csvf/"

def create_csv():
    f = None
    csv_file = csv_path+"fiance-" + \
        datetime.now(timezone(timedelta(hours=+8))
                     ).strftime("%Y-%m")+".csv"
    try :
        f = open(csv_file, 'a' ,newline='')
        writer = csv.writer(f)
        writer.writerow(['date', 'status', 'tag', 'dollar', 'describe'])
        f.close()
    except OSError:
        print("[", datetime.now(), "] can not create the csv file : ",csv_file)
    

def writting(status,tag,dollar ,describe):
    f = None
    csv_file = csv_path+"fiance-" + \
        datetime.now(timezone(timedelta(hours=+8))
                     ).strftime("%Y-%m")+".csv"
    try:
        if not os.path.exists(csv_file):
            raise FileNotFoundError
        else:
            f = open(csv_file, 'a' ,newline='')
    except FileNotFoundError:
        print("[", datetime.now(), "] create the csv file : ",csv_file)
        f = open(csv_file ,'a',newline='')
        writer = csv.writer(f)
        writer.writerow(['date','status','tag','dollar','describe'])
    finally:
        writer = csv.writer(f)
        date = datetime.now(timezone(timedelta(hours=+8))).strftime("%Y-%m-%d")
        writer.writerow([date, status,tag, dollar, describe])
        f.close()
        return 0

def total(year,month):
    
    if month<10 or month>0:
        month = "0"+str(month)
    csv_file = csv_path+"fiance-" +str(year)+"-"+str(month)+".csv"

    try:
        if not os.path.exists(csv_file):
            print("[",datetime.now(),"] the csv file \"",csv_file,"\" not found.")
            raise FileNotFoundError
        else:
            print("[",datetime.now(),"] read the csv file: ",csv_file)
            df = pd.read_csv(csv_file)

            # filter the data from status == pay
            # loc to extract data
            df_filt = (df['status'] == 'pay')
            filt_data = df.loc[df_filt]
            money = filt_data['dollar']

        return sum(money)
    except FileNotFoundError:
        return -1

def lastest_chart():

    today = datetime.now(timezone(timedelta(hours=+8)))
    first = today.replace(day=1)
    lastMonth = first - timedelta(days=1)
    year = lastMonth.strftime("%Y")
    month = lastMonth.strftime("%m")
    
    status = chart.single_chart(status="pay", month=month, year=year)
    
    return status
def monthly_chart(year , month):
    status = chart.single_chart(status="pay", month=month, year=year)
    return status

def list_all(year ,month):
       
    csv_file = csv_path+"fiance-" + str(year)+"-"+str(month)+".csv"
    # print(csv_file)
    try:
        if not os.path.exists(csv_file):
            print("[",datetime.now(),"] the csv file \"",csv_file,"\" not found.")
            raise FileNotFoundError
        else:
            print("[",datetime.now(),"] read the csv file: ",csv_file)
            df = pd.read_csv(csv_file)

            # filter the data from status == pay
            # loc to extract data
            df_filt = (df['status'] == 'pay')
            result = df.loc[df_filt].groupby('tag')

            return result
            
    except FileNotFoundError:
        return None

def compare_chart(y1 ,m1 ,y2 ,m2):
    
    chart.compare_chart("pay",y1,m1,y2,m2)
    


if __name__ == "__main__":
    compare_chart("2022","02","2022","03")
    
