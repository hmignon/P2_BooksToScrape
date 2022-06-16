<p align="center">
    <img src="img/logo_bookstore.png" alt="logo" />
</p>
<h1 align="center">Scraping <em>BooksToScrape</em></h1>
<p align="center">
    <a href="https://www.python.org">
        <img src="https://img.shields.io/badge/Python-3.6+-3776AB?style=flat&logo=python&logoColor=white" alt="python-badge">
    </a>
    <a href="https://www.crummy.com/software/BeautifulSoup/bs4/doc/">
        <img src="https://img.shields.io/badge/BeautifulSoup-4.9+-d71b60?style=flat" alt="Beautiful Soup">
    </a>
    <a href="https://github.com/psf/requests">
        <img src="https://img.shields.io/badge/Requests-2.25+-00838f?style=flat" alt="Requests">
    </a>
</p>

# About the project

**OpenClassrooms Python Developer Project #2: Use Python Basics for Market Analysis**

_Tested on Windows 10, Python 3.9.5._

### Objectives

Scraping of [books.toscrape.com](http://books.toscrape.com) with **BeautifulSoup4** and **Requests**, 
export data to .csv files and download cover images to the *"exports"* folder.

Implementation of the ETL process: 
- **E**xtract relevant and specific data from the source website; 
- **T**ransform, filter and clean data;
- **L**oad data into searchable and retrievable files.

## Post-course optimisation
This project has been optimised after the end of the OpenClassrooms course. 
To view the previously delivered version, please check [this commit](https://github.com/hmignon/P2_mignon_helene/tree/163c5f5b2c730e7b308d01f31479702fb7c1e8e9).

Improvements made to this project include:
- Using OOP for the main scraper
- Optimising loops for faster execution time
- Parsing of command line arguments for options:
  - Json export option
  - Ignore images option
  - One-file export option
- Progress bars (tqdm)

# Usage

### Clone the repository

- `git clone https://github.com/hmignon/P2_mignon_helene.git`

### Create the virtual environment

- `cd P2_mignon_helene`
- `python -m venv env`
- Activate the environment `source env/bin/activate` (macOS and Linux) or `env\Scripts\activate` (Windows)
    
### Install required packages

- `pip install -r requirements.txt`

# Run the project

To scrape the entirety of [books.toscrape.com](https://books.toscrape.com) to .csv files, 
use the command `python main.py`.

## Options

**Use `python main.py --help` to view all options.**

- `--categories`: Scrape one or several categories. This argument takes **category names** and/or **full urls**. 
For example, the 2 following commands would yield the same results:

```
main.py --categories travel
main.py --categories http://books.toscrape.com/catalogue/category/books/travel_2/index.html
```

To scrape a selection of categories, add selected names and/or urls separated by one space.

Note: selecting the same category several times (e.g. `python main.py --categories travel travel`) will only export data once.

```
main.py --categories classics thriller
main.py --categories http://books.toscrape.com/catalogue/category/books/classics_6/index.html thriller
```

- `-c` or `--csv`: Export data to .csv files.
- `-j` or `--json`: Export data to .json files. 

Note: `-j` and `-c` can be used concurrently to export to both formats during the same scraping process.

- `--one-file` : Export all data to a single .csv/.json file.
- `--ignore-covers`: Skip cover images downloads.

## Using .csv files

If you wish to open the exported .csv files in any spreadsheet software (Microsoft Excel, LibreOffice/OpenOffice Calc, Google Sheets...),
please make sure to select the following options:
- UTF-8 encoding 
- comma `,` as *separator*
- double quote `"` as *string delimiter*
