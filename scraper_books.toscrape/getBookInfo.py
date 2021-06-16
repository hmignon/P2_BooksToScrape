# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os
import csv
from categoriesAll import main_url, cat_url, cat_name
import time


def createCsvFile():
    for i in range (len(cat_url)):
        csv_filename = cat_name[i].replace(' ', '_') + ".csv"
        results_directory = 'exports'
        #results_path = os.path.join(results_directory, csv_filename)
        if not os.path.isdir(results_directory):
            os.mkdir(results_directory)
        with open('./exports/'+csv_filename, 'w', encoding='utf-8') as csvfile:
            book_csv = csv.writer(csvfile, delimiter=' ')
            book_csv.writerow(['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])
        getCatPagesUrls(i, csv_filename)


def getCatPagesUrls(i, csv_filename):
    response = requests.get(cat_url[i])
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = int(soup.select_one("form > strong").text)
        if results > 20:
            current_cat_pages = [cat_url[i]]
            page_current = soup.find("li", {'class': "current"}).text
            page_total = int(page_current.strip().replace("Page 1 of ", ""))
            k = 1
            while k < page_total:
                k += 1
                page_url = cat_url[i].replace("index", "page-" + str(k))
                current_cat_pages.append(page_url)
            url_list = []
            print('\n\n' + cat_name[i].strip())
            getBookUrls(current_cat_pages, url_list, i, csv_filename)
            print(str(len(url_list)) + " book(s) exported")       
        else:
            current_cat_pages = [cat_url[i]]
            url_list = []
            print('\n\n' + cat_name[i].strip())
            getBookUrls(current_cat_pages, url_list, i, csv_filename)
            print(str(len(url_list)) + " book(s) exported")
       

def getBookUrls(current_cat_pages, url_list, i, csv_filename):
    for n in range(len(current_cat_pages)):
        response2 = requests.get(current_cat_pages[n])
        soup = BeautifulSoup(response2.text, 'html.parser')
        book_url = [line["href"] for line in soup.select("ol > li > article > h3 > a")]
        for h in range(len(book_url)):
            book_url_clean = main_url + book_url[h].replace("../../../", "catalogue/")
            url_list.append(book_url_clean)
        getProductInfo(url_list, cat_name, i, csv_filename)


# get book info !
def getProductInfo(url_list, cat_name, i, csv_filename):
    for m in range(len(url_list)):
        response3 = requests.get(url_list[m])
        soup = BeautifulSoup(response3.content, 'html.parser')
        product_info = soup.findAll('td')
        upc = product_info[0].text
        pit = product_info[3].text
        pec = product_info[2].text
        available = product_info[5].text
        reviews = product_info[6].text + " review(s)"
        title = str(soup.find('h1').text)
        description = soup.select_one("article > p").text
        img = soup.find("div", {"class": "item active"}).find("img")
        img_url = main_url + img["src"].replace("../../", "")
        #getReviewRating(soup, info)
        info = [url_list[m], upc, title, pit, pec, available, description, cat_name[i], reviews, img_url]
        downloadImages(title, img_url,info, i)
        csvFileAdd(csv_filename, info)
        
        
'''
def getReviewRating(soup, info):
    if soup.find("p", {"class": "star-rating One"}):
        review_rating = "1 star"
    elif soup.find("p", {"class": "star-rating Two"}):
        review_rating = "2 star"
    elif soup.find("p", {"class": "star-rating Three"}):
        review_rating = "3 star"
    elif soup.find("p", {"class": "star-rating Four"}):
        review_rating = "4 star"
    elif soup.find("p", {"class": "star-rating Five"}):
        review_rating = "5 star"
    else:
        review_rating = "no rating"
    info.insert(8, review_rating)
'''


def csvFileAdd(csv_filename, info):
    with open('./exports/'+csv_filename, 'a+', encoding='utf-8') as csvfile:
        book_csv = csv.writer(csvfile, delimiter=' ')       
        book_csv.writerow(info)


def downloadImages(title, img_url, info, i):
    img_directory = 'exports/covers/'
    #characters = [':', '/', u'U+005C', '"', '-', '*', '?']
    #for c in range(len(characters)):
        #clean_title = title.replace(characters[c], '_')
    img_filename = cat_name[i].lower().replace(' ', '_') + "_" + title[:150].replace(':', '_').replace('/', '_').replace(u'U+005C', '_').replace('-', '_').replace('*', '_').replace('?', '_').replace(',', '_').replace('"', '_').replace(' ', '_') + '.jpg'
    img_data = requests.get(img_url).content
    img_path = os.path.join(img_directory, img_filename)
    if not os.path.isdir(img_directory):
        os.mkdir(img_directory)
    file = open(img_path, "wb")
    file.write(img_data)
    #info.append('.../covers/' + img_filename)

    
if __name__ == "__main__":
    startTime = time.time()
    createCsvFile()
    print ('The script took {0} second !'.format(time.time() - startTime))