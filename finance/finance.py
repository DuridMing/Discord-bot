'''
finance csv file operator
'''

from datetime import datetime, timezone, timedelta
import os
import csv
import pandas as pd

def writting(status,dollar ,describe):
    f = None
    path = "finance/"
    csv_file = path+"fiance-" + \
        datetime.now(timezone(timedelta(hours=+8))
                     ).strftime("%Y-%m")+".csv"
    try:
        if not os.path.exists(csv_file):
            raise FileNotFoundError
        else:
            f = open(csv_file, 'a' ,newline='')
    except FileNotFoundError:
        print('First create file: '+csv_file )
        f = open(csv_file ,'a',newline='')
        writer = csv.writer(f)
        writer.writerow(['date','status','dollar','describe'])
    finally:
        writer = csv.writer(f)
        date = datetime.now(timezone(timedelta(hours=+8))).strftime("%Y-%m")
        writer.writerow([date, status, dollar, describe])
        f.close()
        return 0

def total(year,month):
    path = "finance/"
    if month<10 or month>0:
        month = "0"+str(month)
    csv_file = path+"fiance-" +str(year)+"-"+str(month)+".csv"
    try:
        if not os.path.exists(csv_file):
            raise FileNotFoundError
        else:
            df = pd.read_csv(csv_file)

            # filter the data from status == pay
            # loc to extract data
            df_filt = (df['status'] == 'pay')
            filt_data = df.loc[df_filt]
            money = filt_data['dollar']

        return sum(money)
    except FileNotFoundError:
        return -1



if __name__ == "__main__":
    print(total(2022 , 4))