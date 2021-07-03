# -*- coding: utf-8 -*-

"""
-----------------------------------------------------
                      EXPORTS
-----------------------------------------------------
"""

import os
import csv

import requests


def create_csv_file(csv_filename):
    """
    Create 'exports' folder, create .csv file within 'exports' folder
    Write header row in .csv file

    @param csv_filename: category name extracted from category url + .csv extension
    """
    directory = 'exports'
    if not os.path.isdir(directory):
        os.mkdir(directory)
    with open('./exports/' + csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        book_csv = csv.writer(csv_file, delimiter=';')
        book_csv.writerow([
            'product_page_url',
            'universal_product_code',
            'title',
            'price_including_tax',
            'price_excluding_tax',
            'number_available',
            'product_description',
            'category',
            'review_rating',
            'image_url'
        ])


def csv_file_append(csv_filename, info):
    """
    Append extracted book info list to previously created .csv file

    @param csv_filename: category name string extracted from category url + .csv extension
    @param info: list of book information
    """
    with open('./exports/' + csv_filename, 'a+', newline='', encoding='utf-8') as csv_file:
        book_csv = csv.writer(csv_file, delimiter=';')
        book_csv.writerow(info)


def download_images(title, upc, img_url, cat_name):
    """
    Create 'cover_images' folder within 'exports'
    Create folder with current category name in 'cover_images'
    Shorten and clean image file name of invalid characters
    Download and save image as .jpg file

    @param title: current book title string
    @param upc: universal product code string
    @param img_url: current book cover image url string
    @param cat_name: category name string
    """
    img_directory = 'exports/cover_images/'
    img_category_dir = img_directory + cat_name + '/'
    img_name_clean = ''.join([x for x in title[:100] if x.isalnum() or x in ' ']).replace(' ', '_') + '.jpg'
    img_filename = upc + "_" + img_name_clean
    img_data = requests.get(img_url).content

    if not os.path.isdir(img_directory):
        os.mkdir(img_directory)
    img_path = os.path.join(img_category_dir, img_filename)
    if not os.path.isdir(img_category_dir):
        os.mkdir(img_category_dir)

    file = open(img_path, "wb")
    file.write(img_data)
