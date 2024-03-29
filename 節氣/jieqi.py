import sys
import json
import gc
import os
import datetime

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)

class jieqi:
    # 计算节气的C常量组
    C_list_21 = [3.87, 18.73, 5.63, 20.646, 4.81, 20.1, 5.52, 21.04, 5.678, 21.37, 7.108, 22.83, 7.5, 23.13, 7.646, 23.042, 8.318, 23.438, 7.438, 22.36, 7.18, 21.94, 5.4055, 20.12]

    C_list_20 = [4.6295, 19.4599, 6.3826, 21.4155, 5.59,20.888, 6.318, 21.86, 6.5, 22.2, 7.928, 23.65, 8.35,  23.95, 8.44, 23.822, 9.098, 24.218, 8.218, 23.08, 7.9, 22.6, 6.11, 20.84]

    # 节气名称组
    name_Arr = ["立春", "雨水", "驚蟄", "春分", "清明", "穀雨", "立夏", "小滿", "芒種", "夏至", "小暑", "大暑", "立秋", "處暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"]
    
    def __init__(self):
        self.c_list=[]

    ## 特殊年份特殊节气进行纠正
    def rectify_year(self,year,jieqiid,day):
        ## 特殊年份
        rectify_year = [2026,2084,1911,2008,1902,1928,1925,2016,1922,2002,1927,1942,2089,2089,1978,1954,1918,2021,1982,2082,2019,2021]
        ## 特殊节气
        rectify_jieqi = [1,3,6,7,8,9,10,10,11,12,14,15,17,18,19,20,21,21,22,22,23]
        ## 偏移量
        rectify_offset = [-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,-1,-1,1,-1,1]
        pop2 = -1
        if year in rectify_year:
            if year == 2089:
                pop1 = rectify_year.index(year) ## 找到位置
                pop2 = pop1+1
            else:
                pop1 = rectify_year.index(year) ## 找到位置

            if rectify_jieqi[pop1] == jieqiid:
                day = day + int(rectify_offset[pop1])
            if rectify_jieqi[pop2] == jieqiid:
                day = day + int(rectify_offset[pop2])
        return day


    #计算节气日期，并创建文件
    def creat_year_jieqi(self,year):
            year_pre = year//100
            if year_pre == 19:
                C_arr = self.C_list_20
            elif year_pre == 20:
                C_arr = self.C_list_21

            year_num = year%100
            list_arr = {}
            for i in range(0, 24):
                C = C_arr[i]
                ## 注意：凡闰年3月1日前闰年数要减一，即：L=[(Y-1)/4],因为小寒、大寒、立春、雨水这两个节气都小于3月1日,所以 y = y-1
                if i == 0 or i == 1 or i == 22 or i == 23:
                    if self.comrun(year):
                        days = (year_num * 0.2422 + C) // 1 - ((year_num-1)// 4)
                    else:
                        days = (year_num * 0.2422 + C) // 1 - (year_num // 4)
                else:
                    days = (year_num * 0.2422 + C) // 1 - (year_num // 4)

                ## 特殊年份节气进行纠正
                days = self.rectify_year(year,i,days)

                days = int(days)
                days = '%02d' % days
                y = int(year_num // 1)
                m = i // 2 + 2
                if m == 13:
                    m = 1
                m = '%02d' % m
                y = '%02d' % y
                strs2 = "{3}{0}-{1}-{2} 00:00:00".format(str(y), str(m), str(days),str(year_pre))
                d_extracted = strs2[:10]
                #strs =  datetime.datetime.strptime(d_extracted, '%Y-%m-%d')
                item = {d_extracted:self.name_Arr[i]}
                # print (item)
                list_arr.update(item)
            #list_str = json.dumps(list_arr,ensure_ascii=False) ## 中文不进行编码
            #file_name = "./json/{0}.json".format(str(year))
            #with open(file_name, "w",encoding="utf-8") as f:  ## 打开时用 utf-8 编码
                #json.dump(list_str, f,ensure_ascii=False)
                #print("{0}已载入文件完成...".format(str(year)))
            return list_arr
