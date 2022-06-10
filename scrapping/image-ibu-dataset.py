import selenium
from selenium import webdriver
import time
import requests
import os
from PIL import Image
import io
import hashlib

from selenium.webdriver.common.by import By

# This is the path I use
#DRIVER_PATH = '/Users/anand/Desktop/chromedriver'
# Put the path for your ChromeDriver here
DRIVER_PATH = '../driver/geckodriver'


def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:int=1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)    
    
    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    last_number_result = -1
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        
        thumbnail_results = wd.find_elements(by=By.CSS_SELECTOR, value="img.Q4LuWd")
        number_results = len(thumbnail_results)
        if number_results == last_number_result : 
            print('no Incerment')
            break
        last_number_result = number_results
        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
        
        last_img = thumbnail_results[-1]
        ujung = False
        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls    
            actual_images = wd.find_elements(by=By.CSS_SELECTOR, value='img.n3VNCb')
            last_link = ''
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    link = actual_image.get_attribute('src')
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

        if len(image_urls) >= max_links_to_fetch:
            print(f"Found: {len(image_urls)} image links, done!")
            break
        elif ujung :
            print("Sudah di Ujung") 
            break
        else:
            print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(30)

            # return
            load_more_button = wd.find_elements(by=By.CLASS_NAME, value='mye4qd')
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")
                print(wd.execute_script("document.querySelector('.mye4qd').click();"))
            else : 
                print('Ne Image Left.')
                return image_urls
                # parent_load_more_button = wd.find_element_by_class_name('YstHxe')
                # status = parent_load_more_button.get_attribute('style')
                # if status == 'display: none;' :
                #     print("No more Image")
                #     return image_urls

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls

def persist_image(folder_path:str,file_name:str,url:str):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        folder_path = os.path.join(folder_path,file_name)
        if os.path.exists(folder_path):
            file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        else:
            os.mkdir(folder_path)
            file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

if __name__ == '__main__':
    wd = webdriver.Firefox(executable_path=DRIVER_PATH)
    # 'Kalio Ayam', 'Ketoprak', 'Mie Ayam', 'Mie Bakso' , 'Bubur Ayam', 'Beef Teriyaki', 
    queries = ['Bebek Goreng', 'Ayam Taliwang', 'Mie Ayam', 'Martabak Mesir', 'Soto Padang',] 
    # 'Rendang Sapi', 'Sayur Asem', 'Pindang Kenari', 'Sate Bandeng', 'Belut Goreng' ]  #change your set of querries here
    for query in queries:
        wd.get('https://google.com')
        search_box = wd.find_element(by=By.CSS_SELECTOR, value='input.gLFyf')
        search_box.send_keys(query)
        links = fetch_image_urls(query, 1200 ,wd)
        #images_path = '/Users/anand/Desktop/contri/images'  #enter your desired image path
        images_path = './dataset-makanan-ibu-1000/'
        for i in links:
            persist_image(images_path,query,i)
    wd.quit()