import re
import pandas as pd
import difflib

BB1_sum = 0
BB2_sum = 0
input_txt = []
cities = []

inputText = open('bomber_input_BB1_CLEAN_H_C.txt', "r", encoding='utf-8')

for line in inputText:
    input_txt.append(line)

for i in range(0, len(input_txt)):
    if re.findall(r'^[A-K][A-ZÄÖÜ_\s-]{3,}', input_txt[i]) \
            and "°" in input_txt[i + 1]:
        # print(input_txt[i] + input_txt[i+1])
        BB1_sum += 1
        cities.append(input_txt[i].rsplit(' ')[0])

inputText = open('bomber_input_BB2_CLEAN_H_C.txt', "r", encoding='utf-8')

for line in inputText:
    input_txt.append(line)

for i in range(0, len(input_txt)):
    if re.findall(r'^[L-Z][A-ZÄÖÜ_\s-]{3,}', input_txt[i]) \
            and "°" in input_txt[i + 1]:
        # print(input_txt[i] + input_txt[i+1])
        BB1_sum += 1
        cities.append(input_txt[i].rsplit(' ')[0])

#Listenabgleich ab hier
city_data = pd.read_csv(r'city_index_cities.csv', encoding='utf-8')
city_df = pd.DataFrame(city_data)

i = 0
j = 0
while i < len(cities):
    if j == len(city_df.town):
        j = 0
        i +=1
    if cities[i] == city_df.town[j].upper():
        print(cities[i], city_df.page[j], city_df.url_num[j])
        j = 0
        i += 1
    else:
        j +=1