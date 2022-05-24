import pandas as pd
import requests 
from bs4 import BeautifulSoup
from more_itertools import chunked

dataset = pd.read_csv('./resep-ibu.csv')

# print (dataset)

class_List = ['ketoprak']
result_list = []
myList = []

# for i in range(len(dataset['nama'])) :
#     class_List.append(dataset.iloc[i]['nama'])

for class_name in class_List : 
    url = 'https://cookpad.com/id/cari/{class_name}'.format(class_name = class_name)
    html = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    soup = BeautifulSoup(html.content, "html.parser")
    print(soup)

    # for result in soup.find_all('a'):
    #     print(result)

# myList = list(chunked(result_list, 10))
# print (result_list)