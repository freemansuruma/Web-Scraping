

import requests
import pandas as pd
import pymongo
from bs4 import BeautifulSoup
from splinter import Browser
import time


def scrape():

    mars = {}
    news_url = 'https://mars.nasa.gov/news/'
    news_response = requests.get(news_url)

    soup = BeautifulSoup(news_response.text, 'html.parser')

    results = soup.find('li', class_='slide')
    title = soup.find('div', class_ = 'content_title')
    news = soup.find('div', class_='rollover_description_inner')
    news_title = title.a.text
    news_text = news.text
    mars['News_Title'] = news_title
    mars['News_Text'] = news_text

    browser = Browser('chrome', headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    time.sleep(2)
    browser.click_link_by_partial_text('.jpg')
    link = browser.find_by_tag('img')
    mars_image_url = link['src'] 
    mars['Photo_of_the'] = mars_image_url


    weather_url = 'https://twitter.com/marswxreport?lang=en'
    weather_response = requests.get(weather_url)

    w_soup = BeautifulSoup(weather_response.text, 'html.parser')

    tweet = w_soup.find('p', class_= 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    mars_weather = tweet.text
    mars['Mars_Weather'] = mars_weather
   

    facts_url = 'https://space-facts.com/mars/'
    table = pd.read_html(facts_url)
    df_mars = table[0]
    df_mars.set_index(0 ,inplace=True)

    html_table = df_mars.to_html()
    html_table = html_table.replace('\n', ' ')
    mars['Mars_Facts'] = df_mars

    image_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    image_response = requests.get(image_url)

    img_soup = BeautifulSoup(image_response.text, 'html.parser')

    images = img_soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    for image in images:
        link = image.a['href']
        img_response = requests.get('https://astrogeology.usgs.gov'+ link)
        imgSoup = BeautifulSoup(img_response.text, 'html.parser')
        img_item = imgSoup.find('div', class_='downloads')
        img_url = img_item.li.a['href']
        title = image.a.text
        title_url = {'title': title, 'img_url': img_url}
        hemisphere_image_urls.append(title_url)
        
    mars['Mars_Hemispheres'] = hemisphere_image_urls
    
    return mars
        
  

