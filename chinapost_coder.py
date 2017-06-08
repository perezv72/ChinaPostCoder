#!/usr/bin/env python3
import codecs
import time
from selenium import webdriver
import csv
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select

def csvwriter(row):
    with codecs.open('results_wArea2.csv', 'a', 'utf-8') as fout:
        csv_w = csv.writer(fout, delimiter = '|')
        csv_w.writerows(row2)
        fout.close()

driver = webdriver.Chrome()
driver.get("http://cpdc.chinapost.com.cn/web/")
time.sleep(3)
searchbox = driver.find_element_by_id("searchkey")
selcity = Select(driver.find_element_by_name("L_1-2"))
selprov = Select(driver.find_element_by_name("L_1-1"))

tmp = []
city = "city"
province = "prov"
row2 = "包头市"
row3 = "内蒙古自治区"

selprov.select_by_visible_text(row3)
time.sleep(3)
selcity.select_by_visible_text(row2)
time.sleep(1)

with codecs.open("addresses.csv", "r", "utf-8") as f:
    reader = csv.reader(f, delimiter = "\t")
    count = 0
    success = 0
    for row in reader:
        count += 1
        time.sleep(1)
        if city != row[2]:
            print("switching to new city")
            selprov.select_by_visible_text(row[3])
            time.sleep(5)
            selcity.select_by_visible_text(row[2])
            time.sleep(1)
        province = row[3]
        city = row[2]
        try:
            address = row[1]
            searchbox.clear()
            searchbox.send_keys(address)
            driver.find_element_by_id("dosearch").click()
            time.sleep(3)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            try:
                tmpresult = soup.find("ul", {"id":"rstable"})
                result = tmpresult.li.text
                tmpresult2 = soup.find_all("ul", {"id":"rstable"})
                result2 = str(tmpresult2).replace("<li>", ";").replace("</li>", "").replace("</ul>]", "")
                try:
                    postal = result.split(",")[0]
                    if len(postal)==6:
                        success += 1
                        print(str(success) + " of " + str(count) + " found")
                except:
                    continue
            except:
                result = "NA"
                result2 = "NA"
            row.extend([result])
            # if you only want the first result, please remove or comment out the command below.
            row.extend([result2])
            row2 = [row]
            csvwriter(row2)
        except:
            print("computer says no")
            continue

driver.quit()

print("it is done")
