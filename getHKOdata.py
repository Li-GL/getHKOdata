#-*- coding:utf-8 -*-
import urllib
import re
from time import strptime
import os
import csv
from collections import deque
import time

#//////////////////////////////get meterological data//////////////////////////////#
def getMeteData(station):
    global html
    global dateStr
    global latestTime

    url = 'http://www.weather.gov.hk/wxinfo/ts/text_readings_e.htm'
    opener = urllib.urlopen(url)
    html = opener.read()
    opener.close()
    #get date&time
    regexTime = re.compile('Latest readings recorded at (.*) Hong Kong Time (.*)\n')
    matchesTime = re.findall(regexTime, html)
    timeStr = matchesTime[0][0]
    dateList = matchesTime[0][1].split()
    monthNum = str(strptime(dateList[1],'%B').tm_mon)
    dateStr = dateList[-1] + '-' + monthNum + '-' + dateList[0]
    latestTime = dateStr + ' ' + timeStr
    #get data
    regex = re.compile(station+'.*\n')
    matches = re.findall(regex, html)
    data = [re.split(r'\s{3,}',i) for i in matches[:2]]
    temperature = data[0][1]
    humidity = data[0][2]
    windDirection = data[1][1]
    windSpeed = data[1][2]
    windMax = data[1][3].strip('\n')
    #------------------------------write to csv------------------------------#
    current_path = os.getcwd()
    save_path = os.path.join(current_path, 'WeatherData',station)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file= dateStr + '_' + station + '.csv'
    filename = os.path.join(save_path,file)
    # write header
    if not os.path.exists(filename):
        with open(filename,'w') as csvfile:
            fieldnames = ['Datetime', 'Temperature(Celsius)', 'Humidity(%)', 'Wind Direction', 'Wind Speed(km/hour)', 'Maximum Gust(km/hour)']
            writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n',fieldnames=fieldnames)
            writer.writeheader()
    #check datetime, if the data exist, return, no writing to csv
    with open(filename, 'r') as f:
        lastTime = deque(csv.reader(f), 1)[0][0]
    if lastTime == latestTime:
        return 0
        #write data
    with open(filename, 'a') as csvfile:
        fieldnames = ['Datetime', 'Temperature', 'Humidity', 'WindDirection', 'WindSpeed',
                          'MaximumGust']
        writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=fieldnames)
        writer.writerow({'Datetime':latestTime, 'Temperature':temperature, 'Humidity':humidity, \
                         'WindDirection':windDirection, 'WindSpeed':windSpeed,'MaximumGust':windMax})
    returnData = latestTime + '   ' + temperature + u'\u2103' + '   '+ humidity + '%'+ '   ' + 'WD: '+windDirection\
+ '   ' + 'WS: ' + windSpeed +'   ' + 'Max: '+ windMax + '  ||  ' + station
    print returnData
#//////////////////////////////get visibility from the same site//////////////////////////////#
def getVisibility():
    # get visibility data
    regex_visb = re.compile(r'10-Minute Mean Visibility\n\D*(\d{0,})\D*(\d{0,})\D*(\d{0,})\D*(\d{0,})')
    matches_visb = re.findall(regex_visb, html)
    v_central = matches_visb[0][0]
    v_chek = matches_visb[0][1]
    v_sai = matches_visb[0][2]
    v_wag = matches_visb[0][3]
    # ------------------------------write to csv------------------------------#
    current_path = os.getcwd()
    save_path = os.path.join(current_path, 'WeatherData', 'VISIBILITY')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file = dateStr + '.csv'
    filename = os.path.join(save_path, file)
    # write header
    if not os.path.exists(filename):
        with open(filename, 'w') as csvfile:
            fieldnames = ['Datetime', 'Central(km)','Chek Lap Kok(km)','Sai Wan Ho(km)', 'Waglan Island(km)']
            writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=fieldnames)
            writer.writeheader()
    # check datetime, if the data exist, return, no writing to csv
    with open(filename, 'r') as f:
        lastTime = deque(csv.reader(f), 1)[0][0]
    if lastTime == latestTime:
        return 0
    with open(filename, 'a') as csvfile:
        fieldnames = ['Datetime', 'Central(km)','Chek Lap Kok(km)','Sai Wan Ho(km)', 'Waglan Island(km)']
        writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=fieldnames)
        writer.writerow({'Datetime': latestTime, 'Central(km)': v_central,'Chek Lap Kok(km)':v_chek,\
                         'Sai Wan Ho(km)':v_sai, 'Waglan Island(km)':v_wag })
    returnData = 'Visibility:  ' + 'Central '+ v_central + ';'+'  '+'Chek Lap Kok ' + v_chek + ';' +'  '+ 'Sai Wan Ho ' + v_sai +';'\
                    +'  '+ 'Waglan Island ' + v_wag +' km'
    print returnData
#//////////////////////////////main function//////////////////////////////#
HKOstation = ['Wetland Park',  #湿地公园
              'Chek Lap Kok',  #赤鱲角
              'Tuen Mun',      #屯门
              'Shek Kong',     #石岗
              'Tseung Kwan O', # 将军澳
              'Sha Tin',       #沙田
              'Sai Kung',      #西贡
              'Waglan Island', #横澜岛
              'Tsing Yi',      #青衣
              'Ta Kwu Ling',   #打鼓岭
              'Peng Chau',     #坪洲
              'Lau Fau Shan',  #流浮山
               """King's Park""",  #京士柏
              'Cheung Chau'    #长洲

               ]
while True:
    for station in HKOstation:
        try:
            getMeteData(station)
        except:
            continue
    getVisibility()
    time.sleep(300)