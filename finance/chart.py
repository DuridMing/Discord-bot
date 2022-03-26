'''
Finance chart.
using matplotlib.
@author : DuridMing
@date : 03/25/2022
'''
import pandas as pd 
import matplotlib.pyplot as plt 
import os 
from datetime import datetime

def single_chart(status,year ,month):
    
    path = "finance/csvf/"
    csv_file = path+"fiance-" + str(year)+"-"+str(month)+".csv"
    
    try:
        if not os.path.exists(csv_file):
            print("[",datetime.now(),"] the csv file \"",
                  csv_file, "\" not found.")
            raise FileNotFoundError
        else:
            print("[",datetime.now(),"] draw the figure from : "+csv_file)
            df = pd.read_csv(csv_file)

            # filter the data from status == pay
            # loc to extract data
            df_filt = (df['status'] == status )
            data_filt = df.loc[df_filt]

            # print(data_filt)
            plt.figure(figsize=(6, 9))    # 顯示圖框架大小

            dt = data_filt.loc[:,'tag':'dollar'].groupby('tag').sum().to_dict()
            # extrat tag -> trans to dict and extract key
            labels = [*dt['dollar']]      # 製作圓餅圖的類別標籤
            
            # extract value by dict to list
            size = [*dt['dollar'].values()]     # 製作圓餅圖的數值來源

            seprate = [0.07 for i in range(len(labels))]
            plt.pie(size,                         # 數值
                    labels=labels,                # 標籤
                    autopct=lambda p: '{:.2f}%\n({:.0f})'.format(
                        p, (p/100)*sum(size)),
                    pctdistance=0.6,              # 數字距圓心的距離
                    explode=seprate,              # 突出
                    textprops={"fontsize": 12},   # 文字大小
                    shadow=False)                 # 設定陰影


            plt.axis('equal')                                          # 使圓餅圖比例相等
            plt.title( str(year) + "-" + str(month) + " finance chart" ,{"fontsize": 18})  # 設定標題及其文字大小
            plt.legend(loc="best")                                   # 設定圖例及其位置為最佳

            pic_path = "finance/figure/finance-" + \
                str(year) + "-" + str(month) + "-chart.jpg"
            print("[",datetime.now(),"] save figure to :", pic_path)
            plt.savefig(pic_path,   # 儲存圖檔
                        bbox_inches='tight')               # 去除座標軸占用的空間

            plt.close()      # 關閉圖表

        return 0
    except FileNotFoundError:
        return -1
