from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
import time

import os
driverpath = os.path.abspath("chromedriver.exe")
s=Service(executable_path= str(driverpath))

print(os.path.abspath('chromedriver.exe'))
import requests

class App:
    def __init__(self):
        # selenium chrome driver configuration
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2,'profile.default_content_settings.images':2})
        self.driver = webdriver.Chrome(service = s,options=chrome_options)
    
    def scrap(self,link)-> None:
        while(True):
            i= 1
            prev_elems = 0
            next_elems = 10
            per_loop = 10 
            scrapped_data = []
            count_id = 0
            page = 1
            for _ in range(3):
                while(True):
                    SCROLL_PAUSE_TIME = 0.5
                    screen_height = 1080  
                    self.driver.get(link)
                    sleep(3)
                    
                    SCROLL_PAUSE_TIME = 0.5
                    # Get scroll height
                    last_height = self.driver.execute_script("return document.body.scrollHeight")
                    elements = self.driver.find_elements_by_xpath("//table[@class='h7vnx2-2 juYUEZ cmc-table  ']/tbody/tr")
                    # elements = self.driver.find_elements_by_xpath(".//td/div/a/div/div/p[@class='sc-14rfo7b-0 lhJnKD']")
                    for element in elements[prev_elems:next_elems]:
                        count_id=count_id+1
                        try:
                            name= element.find_element(By.XPATH,"./td/div/a/div/div/p[@class='sc-14rfo7b-0 lhJnKD']")
                            price = element.find_element(By.XPATH,"./td/div[@class='sc-131di3y-0 cLgOOr']")
                            row = element.find_elements(By.XPATH,"./td/span[contains(@class,'sc-15yy2pl-0 hzgCfk') or contains(@class,'sc-15yy2pl-0 kAXKAX')]")
                            h_1 = row[0].text
                            h_24 = row[1].text
                            d_7 = row[2].text
                            market_cap = element.find_element(By.XPATH,"./td/p[@class='sc-14rfo7b-0 fVSMmK'] ").text
                            volume = element.find_element(By.XPATH,"./td/div[@class='sc-1prm8qw-0 j3nwcd-0 kLJESq'] /a").text
                            circulating_Supply = element.find_element(By.XPATH,"./td/div[@class='sc-1prm8qw-0 sc-1gslw1d-0 jHWhpv']/div").text
                            data_dict= {
                                'id':count_id,
                                "name":name.text,
                                "price":price.text,
                                "h_1":h_1[0],
                                "h_24":h_24[0],
                                "d_7":d_7,
                                "market_cap":market_cap,
                                "volume":volume,
                                "circulating_Supply":circulating_Supply  
                            }
                            scrapped_data.append(data_dict)
                        except:
                            pass

                    temp= next_elems
                    prev_elems = temp
                    next_elems = prev_elems + per_loop

                    self.driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
                    i += 1
                    time.sleep(SCROLL_PAUSE_TIME)
        
                    scroll_height = self.driver.execute_script("return document.body.scrollHeight;")
                    if (screen_height) * i > scroll_height:
                        break            
            page += 1
            self.driver.maximize_window()
            buttons = self.driver.find_elements_by_xpath("//div[@class='sc-1t7mu4i-0 kbMknJ']/ul/li")
            for b in buttons:
                if b.text==str(page):
                    b.click()
                    sleep(3)
                    break
            

            url = "http://127.0.0.1:5000/update-record"
            data = scrapped_data
            response = requests.post(url, json=data )
            print("Status Code", response.status_code)
        
        def close(self)-> None:
            self.driver.close()
        
        
a = App()
a.scrap("https://coinmarketcap.com")
# a.close()

