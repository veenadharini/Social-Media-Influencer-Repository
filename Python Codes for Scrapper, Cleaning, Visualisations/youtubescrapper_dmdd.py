from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver.common.by import By
import pandas as pd
import json


#setting firefox window
option = Options()
option.headless = False
driver = webdriver.Firefox(options=option)
driver.implicitly_wait(5)

#scraper will open firefox and run for youtube
baseUrl = "https://youtube.com/"



#based on keyword result, this method will get all channel URLS that show in results
def getChannelUrl():
    driver.get(f"{baseUrl}/search?q={keyword}")
    time.sleep(2)   
    allChannelList= driver.find_elements(By.CSS_SELECTOR,"#text.style-scope.ytd-channel-name a.yt-simple-endpoint.style-scope.yt-formatted-string")
    links = list(dict.fromkeys(map(lambda a: a.get_attribute("href"),allChannelList)))
    return links

#based each URL fetched in above method, the below method will open about page of youtuber and fetch parameters such as name, handle, url, desciption, subscribers, joining date, views, country, category
def getChannelDetails(urls):   
    for url in urls:
        driver.get(f"{url}/about")
        cname = driver.find_element(By.CSS_SELECTOR,"#text.style-scope.ytd-channel-name").text
        chandle = driver.find_element(By.CSS_SELECTOR,"#channel-handle.meta-item.style-scope.ytd-c4-tabbed-header-renderer").text
        cDess = driver.find_element(By.CSS_SELECTOR,"#description-container > yt-formatted-string:nth-child(2)").text
        csubscriber = driver.find_element(By.CSS_SELECTOR, "#subscriber-count.meta-item.style-scope.ytd-c4-tabbed-header-renderer").text
        clink = url
        otherLinkObj = driver.find_elements(By.CSS_SELECTOR,"#link-list-container.style-scope.ytd-channel-about-metadata-renderer a.yt-simple-endpoint.style-scope.ytd-channel-about-metadata-renderer")
        otherLinks = list(dict.fromkeys(map(lambda a: a.get_attribute("href"),otherLinkObj)))
        cjoined = driver.find_element(By.CSS_SELECTOR,"#right-column > yt-formatted-string:nth-child(2)").text
        cviews = driver.find_element(By.CSS_SELECTOR,"#right-column > yt-formatted-string:nth-child(3)").text
        ccountry = driver.find_element(By.CSS_SELECTOR,"#details-container.style-scope.ytd-channel-about-metadata-renderer").text 
        obj = {
            "name" : cname,
            "handle" : chandle,
            "url"  : clink,
            "desc" : cDess,
            "subscribers" : csubscriber,
            "otherLinks" : otherLinks,
            "joined on" : cjoined,
            "total views" : cviews,
            "country" : ccountry,   
            "type" : keyword 
        }

        

        details.append(obj)
    return details

#based on URL fetched in above method, the below method will open about page of youtuber and fetch description, url, handle of youtuber
def getChannelViews(urls):
    
    for url in urls:
        driver.get(f"{url}/videos")
        cdesc = driver.find_element(By.CSS_SELECTOR,"#video-title-link.yt-simple-endpoint.focus-on-expand.style-scope.ytd-rich-grid-media").text
        chandle = driver.find_element(By.CSS_SELECTOR,"#channel-handle.meta-item.style-scope.ytd-c4-tabbed-header-renderer").text
        clink = url
        obj1 = {
            "description" : cdesc,
            "handle" : chandle,
            "url"  : clink
            }

        cols.append(obj1)
    return cols


if __name__ == "__main__":
    details = []
    cols = []
    #setting keywords for which data of profiles needs to be fetched
    keywords = ["kim kardashian","Dance","Business","Lifestyle","Travel","Technology"]
    for x in keywords:
        keyword = x
        allChannelUrls = getChannelUrl()
        allChannelDetails = getChannelDetails(allChannelUrls)
        allChannelViews = getChannelViews(allChannelUrls)
    
    df = pd.DataFrame(allChannelDetails) 
    df1 = pd.DataFrame(allChannelViews)
    #exporting data frames to csv
    df.to_csv('youtube_profile.csv')
    df1.to_csv('youtube_details.csv')