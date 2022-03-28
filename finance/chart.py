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
import numpy as np 

from config import *

# DATA_PATH = "data/"

csv_path = DATA_PATH+"csvf/"
fig_path = DATA_PATH+"figure/"

def csv2df_by_status(cpath ,status):
    try:
        if not os.path.exists(cpath):
            print("[", datetime.now(), "] the csv file \"",
                  cpath, "\" not found.")
            raise FileNotFoundError
    except FileNotFoundError:
        return -1

    df = pd.read_csv(cpath)
    print("[",datetime.now(),"] read the file: ",cpath)

    # filter the data from status == pay
    # loc to extract data
    df_filt = (df['status'] == status )
    data_filt = df.loc[df_filt]

    return data_filt


def DF_sumBytag(df:pd.DataFrame , tag):
    # extrat tag -> trans to dict and extract key
    gbdf = df.loc[:, 'tag':tag].groupby('tag').sum().to_dict()

    # extract key
    labels = [*gbdf[tag]]

    # extract values
    size = [*gbdf[tag].values()]

    return labels , size

def tck(labels, size):
    tagcheck = ['food', 'book', 'game', 'necessary', 'traffic', 'other']
        
    if (list(set(tagcheck) - set(labels))) is not None:
        dif = list(set(tagcheck) - set(labels)) 
        for i in dif:
            ins = tagcheck.index(i)
            labels.insert(ins, i)
            size.insert(ins, 0)
        
    return labels , size


def single_chart(status,year ,month):
    
    csv_file = csv_path+"fiance-" + str(year)+"-"+str(month)+".csv"

    data_filt = csv2df_by_status(csv_file , "pay")

    print("[", datetime.now(), "] draw new figure : finance-"+str(year) + "-" + str(month) + "-chart.jpg")
    # labels 圓餅圖的標籤
    # size 圓餅圖的數值
    labels ,size = DF_sumBytag(data_filt, "dollar")

    plt.figure(figsize=(6, 9))    # 顯示圖框架大小

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

    pic_path = fig_path+"/finance-" + \
        str(year) + "-" + str(month) + "-chart.jpg"
    print("[",datetime.now(),"] save figure to :", pic_path)
    plt.savefig(pic_path,              # 儲存圖檔
                 bbox_inches='tight')  # 去除座標軸占用的空間

    plt.close()      # 關閉圖表

    return 0

# compare chart using histergram
def compare_chart(status,y1 ,m1 ,y2 ,m2):
    csv_file1 = csv_path+"fiance-" + str(y1)+"-"+str(m1)+".csv"
    csv_file2 = csv_path+"fiance-" + str(y2)+"-"+str(m2)+".csv"

    fdata1 = csv2df_by_status(csv_file1 , "pay")
    fdata2 = csv2df_by_status(csv_file2 , "pay")

    labels1, size1 = DF_sumBytag(fdata1, "dollar")
    labels2, size2 = DF_sumBytag(fdata2, "dollar")

    labels1, size1 = tck(labels1 , size1)
    labels2, size2 = tck(labels2 , size2)

    lsdf = pd.DataFrame({'tags': labels1, 
                        str(y1)+"-" + str(m1): size1, 
                        str(y2)+"-"+str(m2): size2})
    
    print("[", datetime.now(), "] draw new figure : finance-""compare-" +
            str(y1)+"-"+str(m1)+"-and-"+str(y2)+"-"+str(m2)+"-chart.jpg")

    # figure setting
    fig, ax = plt.subplots()
    fig.set_size_inches(9, 5)

    width = 0.35 
    x = np.arange(len(lsdf['tags']))

    # plt.text set position
    rects1 = ax.bar(x - width/2, lsdf[str(y1)+"-"+str(m1)], 
                    width, 
                    label=str(y1)+"-"+str(m1))
    rects2 = ax.bar(x + width/2, lsdf[str(y2)+"-"+str(m2)], 
                    width, 
                    label=str(y2)+"-"+str(m2))

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('NTD')
    ax.set_title("compare "+str(y1)+"-"+str(m1)+" and "+str(y2)+"-"+str(m2))
    ax.set_xticks(x, lsdf['tags'])
    ax.legend()
    
    # add labes 
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    pic_path = fig_path+"finance-" + \
        "compare-"+str(y1)+"-"+str(m1)+"-and-"+str(y2)+"-"+str(m2)+"-chart.jpg"
    print("[", datetime.now(), "] save figure to :", pic_path)
    plt.savefig(pic_path) # save





# need a function to draw fig. about compare two month data.
# use histergram. 