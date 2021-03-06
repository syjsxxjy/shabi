#!/usr/bin/python
# -*- coding: UTF-8 -*-
from openpyxl import Workbook
import time

#创建一个工作表
wb = Workbook()

def creatxls():
#找到活动的sheet页。空的excel表默认的sheet页就叫Sheet，如果想改名字，可以直接给title属性赋值。
    sheet = wb.active
    sheet.title = "Temperature"

    #往sheet页里面写内容
    sheet['A1'] = '温度测量结果'
    sheet['E1'] = 'キ ヨク　Ji Yi'
    timestr=str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    sheet['C1'] = timestr

    sheet['A3'] = '温度(60℃)'
    sheet['A4'] = 'Pt1000測定'
    sheet['B4'] = '温度センサー測定'

    sheet['C3'] = '温度(70℃)'
    sheet['C4'] = 'Pt1000測定'
    sheet['D4'] = '温度センサー測定'

    sheet['E3'] = '温度(90℃)'
    sheet['E4'] = 'Pt1000測定'
    sheet['F4'] = '温度センサー測定'

    
    #公式操作
    #   sheet["A%d" % (i+1)].value = i + 1
    # for i in range(10):
    # sheet["E1"].value = "=SUM(A:A)"


    
#保存
def save(filename):
    wb.save(filename)

if __name__ == '__main__':
    creatxls()
    save("%s保存一个新的xls.xlsx"%str(time.strftime('%H:%M:%S %Y-%m-%d',time.localtime(time.time()))))
    print("执行完毕")


