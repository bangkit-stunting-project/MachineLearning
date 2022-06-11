import os
from unittest import result
import requests
import selenium 
from selenium import webdriver
import time 
import requests
from PIL import Image
import io 
import hashlib

from selenium.webdriver.common.by import By 

DRIVER_PATH = '../driver/geckodriver'

driver = webdriver.Firefox(executable_path=DRIVER_PATH)
queries = ['Abon Ikan', 'Tekwan'] 

for query in queries : 
    driver.get('https://google.com')
    search_box = driver.find_element(by=By.CSS_SELECTOR, value='input.gLFyf')
    search_box.send_keys(query)

    link = []
    max_scrapping_data = 1200

    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
    driver.get(search_url.format(q=query))

    image_count = 0
    result_start = 0
    last_len = len(link)

    while image_count < max_scrapping_data : 
        load_button_style = driver.find_element(by=By.CLASS_NAME, value='YstHxe').get_attribute('style')
        # while load_button_style == 'display: none;':
            # load_button_style = driver.find_element(by=By.CLASS_NAME, value='YstHxe').get_attribute('style')
            # print(load_button_style)
        for i in range(5) : 
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(1)
            # if load_button_style == "" : 
                # break

        thumbnail_result = driver.find_elements(by=By.CSS_SELECTOR, value='img.Q4LuWd')
        number_result = len(thumbnail_result)
        print(f"Ketemu {number_result} gambar. Extracting link dari {result_start}:{number_result}")

        for img in thumbnail_result[result_start:number_result] :
            try : 
                img.click()
                time.sleep(1)
            except Exception : 
                continue 

            actual_images = driver.find_elements(by=By.CSS_SELECTOR, value='img.n3VNCb')

            for actual_image in actual_images : 
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    link.append(actual_image.get_attribute('src'))
            
            image_count = len(link)
        
        if len(link) >= max_scrapping_data : 
            print (f'Ketemu {len(link)} link, Selesai')
            if last_len == len(link) : 
                break
            else : break 
        else : 
            print(f'Ketemu {len(link)}, sisa {max_scrapping_data-len(link)} data lagi')
            time.sleep(20)

            load_more_btn = driver.find_elements(by=By.CLASS_NAME, value='mye4qd')
            if load_more_btn : 
                driver.execute_script("document.querySelector('.mye4qd').click();")
            
        last_len = len(link)
        result_start = len(thumbnail_result)

    saved_path = './dataset-makanan-ibu-1000'
    for i, url in enumerate(link) : 
        try : 
            image_content = requests.get(url).content
        except Exception as e : 
            print (f"ERROR - Gambar ke{i} di {url} ga bisa di download. Detail {e}")

        try : 
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            folder_path = os.path.join(saved_path, query)
            if os.path.exists(folder_path) : 
                file_path = os.path.join(folder_path, hashlib.sha1(image_content).hexdigest()[:10] + '-' + query + '.jpg')
            else : 
                os.mkdir(folder_path)
                file_path = os.path.join(folder_path, hashlib.sha1(image_content).hexdigest()[:10] + '-' + query + '.jpg')
            with open(file_path, 'wb') as f: 
                image.save(f, "JPEG", quality=85)
            print(f"SUKSES - Gambar ke {i} di {url} tersimpan di {file_path}")
        except Exception as e : 
            print(f"ERROR - Gambar ke{i} di {url} gabisa disimpan. Detail {e}")
driver.quit()
