# -*- coding: utf-8 -*-

"""
-----------------------------------------------------
                EXTRACT BOOK DATA
-----------------------------------------------------
"""

import requests
from bs4 import BeautifulSoup

from export_data import csv_file_append, download_images


def get_book_info(book_url, cat_name, csv_filename):
    """
    Get book information and add it to a list

    @param book_url: book url string
    @param cat_name: category name string
    @param csv_filename: category name string extracted from category url
    """
    response = requests.get(book_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_info = soup.find_all('td')
    upc = product_info[0].text
    pit = product_info[3].text
    pet = product_info[2].text
    available = product_info[5].text
    title = str(soup.find('h1').text)

    description = soup.select_one("article > p").text.replace(' ...more', '')
    review_rating = get_review_rating(soup.select_one('.star-rating').attrs['class'][1])
    img = soup.find("div", {"class": "item active"}).find("img")
    img_url = img["src"].replace("../../", "https://books.toscrape.com/")

    info = [book_url, upc, title, pit, pet, available, description, cat_name, str(review_rating) + " star(s)", img_url]

    csv_file_append(csv_filename, info)
    download_images(title, img_url, cat_name)


def get_review_rating(rating):
    """
    Compare star rating string to possible ratings list elements
    Convert rating into integer

    @param rating: star rating string
    @return: rating type int
    """
    ratings = ['One', 'Two', 'Three', 'Four', 'Five']
    for i, letter in enumerate(ratings):
        if rating == letter:
            return i + 1
