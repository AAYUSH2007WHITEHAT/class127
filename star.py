from bs4 import BeautifulSoup
import time
import csv
import pandas as pd
import requests
import csv

START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser = webdriver.Chrome("/Users/apoorvelous/Downloads/chromedriver")
browser.get (START_URL)
time.sleep(10)
headers = ["name", "distance" , "mass", "radius",]
star_data= []
def scrape ():
    for i in range (1,5) :
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            current_page_num= int(soup.find_all("input",attrs={"class", "page_num"})[0].get("value"))
            if current_page_num < i :
                 browser.find_element(BY.XPATH,value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_num > i:
                 browser.find_element(BY.XPATH,value='//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()    
            else:
                break     
        
        for ul_tag in soup.find_all("ul", attrs={"class","exoplanet"}):
            li_tag = ul_tag.find_all("li")
            temp_list=[]
            for index, li_tag in enumerate (li_tag):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            hyperlink_li_bag = li_tag[0]
            temp_list.append("https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"+ hyperlink_li_bag.find_all("a",href=True)[0]["href"])
            star_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
   
scrape()
new_star_data =[]
def scrape_more_data(hyperlink):
   try:
       page=requests.get(hyperlink)
       soup = BeautifulSoup(browser.page_source, "html.parser")
       temp_list=[]
       for tr_tag in soup.find_all("tr", attrs={"class":"fact_row"}):
            td_tags = td_tags.find_all("td")
            for td_tags in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs={"class":"value"})[0].contents[0])
                except:
                     temp_list.append("")
       new_star_data.append(temp_list)
   except:
        time.sleep(1)
        scrape_more_data(hyperlink)
for inex,data in enumerate(star_data):
    scrape_more_data(data[5])
final_planet_data = []
for index, data in enumerate (star_data):
    new_element=new_star_data[index]
    new_element=[elem.replace("\n","")for elem in new_element]
    new_element=new_element[:7]
    final_planet_data.append(data+new_element)           
                                            
       
       
       

with open("final.csv", "w" ) as f :    
                csvwriter=csv.writer(f)
                csvwriter.writerow(headers)
                csvwriter.writerows(final_planet_data)