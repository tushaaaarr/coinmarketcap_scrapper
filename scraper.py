from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
import time

import os
driverpath = os.path.abspath(os.getcwd())+"/chromedriver.exe"
s=Service(executable_path= str(driverpath))
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
            SCROLL_PAUSE_TIME = 0.5
            self.driver.get(link)
            sleep(3)
            try:
                self.driver.find_element(By.CLASS_NAME,"css-1pcqseb").click()
            except:
                pass
            page = 1
            count_id = 0
            scrapped_data = []
            elements = self.driver.find_elements_by_xpath("//table[@class='h7vnx2-2 juYUEZ cmc-table  ']/tbody/tr")
            for element in elements:
                count_id = count_id + 1
                try:
                    name= element.find_element_by_xpath("./td/div/a/div/div/p[@class='sc-14rfo7b-0 lhJnKD']")
                    price = element.find_element_by_xpath("./td/div[@class='sc-131di3y-0 cLgOOr']")
                    row = element.find_elements_by_xpath("./td/span[contains(@class,'sc-15yy2pl-0 hzgCfk') or contains(@class,'sc-15yy2pl-0 kAXKAX')]")
                    h_1 = row[0].text,
                    h_24 = row[1].text,
                    d_7 = row[2].text
                    market_cap = element.find_element_by_xpath("./td/p[@class='sc-14rfo7b-0 fVSMmK'] ").text
                    volume = element.find_element_by_xpath("./td/div[@class='sc-1prm8qw-0 j3nwcd-0 kLJESq'] /a").text
                    circulating_Supply = element.find_element_by_xpath("./td/div[@class='sc-1prm8qw-0 sc-1gslw1d-0 jHWhpv']/div").text
                    
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

                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(SCROLL_PAUSE_TIME)

                except:
                    count_id = count_id-1
                    pass
            

            url = "http://127.0.0.1:5000/update-record"
            data = scrapped_data
            response = requests.post(url, json=data )
            print("Status Code", response.status_code)
            # print(data)

            # time.sleep(300)

        def close(self)-> None:
            self.driver.close()
        
        

a = App()
a.scrap("https://coinmarketcap.com")
a.close()

