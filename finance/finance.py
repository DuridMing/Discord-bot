'''
finance csv file operator
'''

from datetime import datetime, timezone, timedelta
import os
import csv
import pandas as pd

import finance.chart as chart
# import chart

def writting(status,tag,dollar ,describe):
    f = None
    path = "finance/csvf/"
    csv_file = path+"fiance-" + \
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
    # print("counting total.")
    path = "finance/csvf/"
    if month<10 or month>0:
        month = "0"+str(month)
    csv_file = path+"fiance-" +str(year)+"-"+str(month)+".csv"

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
    
    # path = "finance/figure/"
    # pic_path = path+"finance-" + str(year)+"-"+str(month)+"-chart.jpg"

    status = chart.single_chart(status="pay", month=month, year=year)
    
    return status
    

if __name__ == "__main__":
    print(total(2022,3))