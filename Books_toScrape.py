# -*- coding: utf-8 -*-

'''
===================================================================
            SCRAPING BOOKS.TOSCRAPE.COM

This program will scrape books information from books.toscrape.com 
with BeautifulSoup4, export the data to csv files and download the 
cover images to an 'exports' folder
===================================================================


'''

import time
import requests
import os
import csv
import re
from bs4 import BeautifulSoup




'''
-----------------------------------------------------
                GET USER INPUT
Prompt the user to choose whether they want to scrape 
the entire website or only one category.
-----------------------------------------------------
'''

def main():
    print("\n\n-----------------------------")
    print("\n Scraping books.toscrape.com\n")
    print("-----------------------------\n\n")
    time.sleep(1)
    main_url = 'https://books.toscrape.com/'
    response = requests.get(main_url)
    if response.status_code == 200:
        print("\n- connection ok -")
        soup = BeautifulSoup(response.text, 'html.parser')
        cat_name_list = [line.text.strip() for line in soup.select("ul > li > ul > li > a")]
        cat_url_list = [main_url + line["href"] for line in soup.select("ul > li > ul > li > a")]



    url = input('\n\nPaste the url you would like to scrape : ')
    startTime = int(time.time())

    if url.replace('index.html', '') == main_url:
        print("\nExporting all categories...\n")
        time.sleep(1)
        for i in range(len(cat_url_list)):
            getCatPagesUrls(cat_url_list[i])
        print('All books exported in {0} seconds.'.format(int(time.time()) - startTime))
        print('\n------END------')

    elif url in cat_url_list:
        index = cat_url_list.index(url)
        cat_url_list = [cat_url_list[index]]
        cat_name_list = [cat_name_list[index]]
        getCatPagesUrls(cat_url_list[0])
        print('\n\nAll books exported in {0} seconds.'.format(int(time.time()) - startTime))
        time.sleep(1)
        print('\n------END------')






'''
-----------------------------------------------------
                EXTRACT CATEGORY INFO
-----------------------------------------------------
'''

def getCatName(cat_url):
    cat_name = cat_url.replace('https://books.toscrape.com/catalogue/category/books/', '').replace('/index.html', '').replace('_', '').replace('-', ' ')
    cat_name = re.sub(r'[0-9]+', '', cat_name)  # remove all numbers from the string
    print("\nExporting " + cat_name.title() + "\n")
    return cat_name


# get urls for all pages in each category
def getCatPagesUrls(cat_url):
    cat_name = getCatName(cat_url)
    response = requests.get(cat_url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        books_total = int(soup.select_one("form > strong").text)
        if books_total > 20:
            page_total = int(soup.find("li", {"class":"current"}).text.replace("Page 1 of", ""))
        else:
            page_total = 1

    csv_filename = cat_name.lower().replace(' ', '_') + ".csv"
    createCsvFile(csv_filename)

    page_url = cat_url
    current_cat_pages = [page_url]
    for page in range(page_total):
        if page == 0:
            book_url_list = getBookUrls(current_cat_pages[0])
            for k in range(len(book_url_list)):
                getBookInfo(book_url_list[k], cat_name, csv_filename)           
        else:
            current_cat_pages.append(page_url.replace("index", "page-" + str(page+1)))
            book_url_list = getBookUrls(current_cat_pages[page])
            for k in range(len(book_url_list)):
                getBookInfo(book_url_list[k], cat_name, csv_filename)

    print(str(books_total) + " book(s) exported\n\n")
    print("-----------------------------------------------")
         



# get urls of all books in each page
def getBookUrls(cat_page):
    response = requests.get(cat_page)
    soup = BeautifulSoup(response.text, 'html.parser')
    book_url_list = []
    book_url = [line["href"] for line in soup.select("ol > li > article > h3 > a")]
    for book in range(len(book_url)):
        book_url_clean = book_url[book].replace("../../../", "https://books.toscrape.com/catalogue/")
        book_url_list.append(book_url_clean)

    return book_url_list

    
    





'''
-----------------------------------------------------
                EXTRACT BOOK DATA
-----------------------------------------------------
'''

def getBookInfo(book_url, cat_name, csv_filename):
    response = requests.get(book_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_info = soup.find_all('td')
    upc = product_info[0].text
    pit = product_info[3].text
    pet = product_info[2].text
    available = product_info[5].text
    title = str(soup.find('h1').text)


    description = soup.select_one("article > p").text
    review_rating = getReviewRating(soup.select_one('.star-rating').attrs['class'][1])
    img = soup.find("div", {"class": "item active"}).find("img")
    img_url = img["src"].replace("../../", "https://books.toscrape.com/")

    info = [book_url, upc, title, pit, pet, available, description, cat_name, str(review_rating)+" star(s)", img_url]

    csvFileAppend(csv_filename, info)
    downloadImages(title, img_url, cat_name)



def getReviewRating(rating):
    ratings = ['One', 'Two', 'Three', 'Four', 'Five']
    for i, str in enumerate(ratings):
        if rating == str:
            return i+1






'''
-----------------------------------------------------
                      EXPORTS
-----------------------------------------------------
'''

def createCsvFile(csv_filename):
    books_total_directory = 'exports'
    if not os.path.isdir(books_total_directory):
        os.mkdir(books_total_directory)
    with open('./exports/'+csv_filename, 'w', encoding='utf-8') as csvfile:
        book_csv = csv.writer(csvfile, delimiter=' ')
        book_csv.writerow(['product_page_url', 'universal_product_code', 'title', 'price_including_tax',
                              'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])
    


def csvFileAppend(csv_filename, info):
    with open('./exports/'+csv_filename, 'a+', newline='', encoding='utf-8') as csvfile:
        book_csv = csv.writer(csvfile, delimiter=' ')       
        book_csv.writerow(info)



def downloadImages(title, img_url, cat_name):
    img_directory = 'exports/cover_images/'
    img_category_dir = img_directory + cat_name + '/'
    img_filename = ''.join([x for x in title[:150] if x.isalnum() or x in ' ']).replace(' ', '_') + '.jpg'      # remove all non-alphanumeric characters
    img_data = requests.get(img_url).content

    if not os.path.isdir(img_directory):
        os.mkdir(img_directory)
    img_path = os.path.join(img_category_dir, img_filename)
    if not os.path.isdir(img_category_dir):
        os.mkdir(img_category_dir)

    file = open(img_path, "wb")
    file.write(img_data)





if __name__ == "__main__":
    main()

