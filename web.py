from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
import csv 

url = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"

browser = webdriver.Chrome("C:\DHRUV\Whitehat Projects\Class projects\Web scrapping\chromedriver_win32\chromedriver.exe")

browser.get(url)
headers = ["planet name" , "light year from earth" , "planet mass","steller magnitude","Discovery date","hyperlink","Planet Type","planet radius","orbital radius","orbital period","eccentricity"]
planet_Data = []
new_planet_data = []
def scrap ():
    for i in range (1,199):
        while True:
            soup = BeautifulSoup(browser.page_source,"html.parser")
            currentPageNumber = int (soup.find_all("input", attrs ={"class", "page_num"} )[0].get("value"))
            if currentPageNumber < i :
                browser.find_element_by_xpath("/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[2]/a").click()
            elif currentPageNumber > i :
                browser.find_element_by_xpath("/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[1]/a").click()
            else:
                break
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}): 
            li_tags = ul_tag.find_all("li") 
            temp_list = [] 
            for index, li_tag in enumerate(li_tags): 
                if index == 0: 
                    temp_list.append(li_tag.find_all("a")[0].contents[0]) 
                else: 
                    try:
                        temp_list.append(li_tag.contents[0]) 
                    except: 
                        temp_list.append("") 
            hyperlink_li_tag = li_tags[0] 
            temp_list.append("https://exoplanets.nasa.gov"+hyperlink_li_tag.find_all("a", href=True)[0]["href"]) 
            planet_Data.append(temp_list) 

        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click() 
        print(f"{i} page done 1")


def scrap_more_data(hyperlink) :
    try :
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content,"html.parser")
        all_tr_tag = soup.find_all("tr",attrs = {"class","fact_row"})
        templist =[]
        for tr_tag in all_tr_tag:
            all_td_tag = tr_tag.find_all("td")
            for td_tag in all_td_tag:
                contents = td_tag.find_all("div",attrs={"class","value"})[0].contents[0]
                templist.append(contents)
        new_planet_data.append(templist)
    except: 
        time.sleep(1)
        scrap_more_data(hyperlink)

scrap()


for index,data in enumerate(planet_Data):
    scrap_more_data(data[5])
    print(f"{index+1}page done 2")
final_planet_data= []

for index,data in enumerate(new_planet_data):
    new_planet_data_element = new_planet_data[index]
    new_planet_data_element = [elem.replace("\n", "") for elem in new_planet_data_element]
    new_planet_data_element = new_planet_data_element[0:7]
    final_planet_data.append(planet_Data[index]+new_planet_data_element)

with open("scrapper.csv","w") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(final_planet_data)

    
    
