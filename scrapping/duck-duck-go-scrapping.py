import DuckDuckGoImages as ddg
import os 

max_urls = 1000
path = './dataset-makanan-ibu-1000/'
class_list = ['']

for i in class_list : 
    data_path = os.path.join(path, i) 
    if not os.path.exists(data_path) :
        os.mkdir(data_path)
    ddg.download(i, folder=data_path, max_urls=max_urls)

# ddg.download('Martabak Mesir', folder='./dataset-makanan-ibu-1000/Martabak Mesir/', max_urls=1000)