# -*- coding: utf-8 -*-

"""
-----------------------------------------------------
                EXTRACT CATEGORY INFO
-----------------------------------------------------
"""

import re

import requests
from bs4 import BeautifulSoup

from book_info import get_book_info
from export_data import create_csv_file


def get_cat_name(cat_url):
    """
    Get category name from category url string

    @param cat_url: category url string
    @return: category name string
    """
    cat_name = cat_url.replace('https://books.toscrape.com/catalogue/category/books/', '')
    cat_name = cat_name.replace('/index.html', '').replace('_', '').replace('-', ' ')
    cat_name = re.sub(r'[0-9]+', '', cat_name)

    print("\nExporting " + cat_name.title() + "\n")
    return cat_name


def get_cat_pages_urls(cat_url):
    """
    Get total number of books in current category
    if more than 20 books: get total amount of pages
    else: total = 1 page
    Create .csv file
    For each page, get book urls

    @param cat_url: category url string
    """
    cat_name = get_cat_name(cat_url)
    response = requests.get(cat_url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        books_total = int(soup.select_one("form > strong").text)
        if books_total > 20:
            page_total = int(soup.find("li", {"class": "current"}).text.replace("Page 1 of", ""))
        else:
            page_total = 1

        csv_filename = cat_name.lower().replace(' ', '_') + ".csv"
        create_csv_file(csv_filename)

        page_url = cat_url
        current_cat_pages = [page_url]
        for page in range(page_total):
            if page == 0:
                book_url_list = get_book_urls(current_cat_pages[0])
                for k in range(len(book_url_list)):
                    get_book_info(book_url_list[k], cat_name, csv_filename)
            else:
                current_cat_pages.append(page_url.replace("index", "page-" + str(page + 1)))
                book_url_list = get_book_urls(current_cat_pages[page])
                for k in range(len(book_url_list)):
                    get_book_info(book_url_list[k], cat_name, csv_filename)

        print(str(books_total) + " book(s) exported\n\n")
        print('-----------------------------------------------')


def get_book_urls(cat_page):
    """
    For each page, add clean book url to a list

    @param cat_page: current category page url string
    @return: list of book urls in page
    """
    response = requests.get(cat_page)
    soup = BeautifulSoup(response.text, 'html.parser')
    book_url_list = []
    book_url = [line["href"] for line in soup.select("ol > li > article > h3 > a")]
    for book in range(len(book_url)):
        book_url_clean = book_url[book].replace("../../../", "https://books.toscrape.com/catalogue/")
        book_url_list.append(book_url_clean)

    return book_url_list
