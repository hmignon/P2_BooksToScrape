import argparse
import time

from scraper import BookScraper


def timer(start):
    """Calculate and print scraping process time."""
    end_time = int(time.time()) - start
    print(f"\n\nAll done! Books exported in {end_time // 60} mins {end_time % 60} secs.")


def main():
    """Init arg parser, and start scraper with config vars."""
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-c", "--csv", action="store_true", help="Export to csv files")
    parser.add_argument("-j", "--json", action="store_true", help="Export to json files")
    parser.add_argument("--one-file", action="store_true", help="Export data to one csv file")
    parser.add_argument("--ignore-covers", action="store_true", help="Skip cover downloads")
    parser.add_argument("--categories", type=str, nargs="+", default=None,
                        help="Scrape specific categories (name or full url)")
    args = parser.parse_args()
    config = vars(args)
    if not config["json"] and not config["csv"]:
        config["csv"] = True

    start = int(time.time())
    scraper = BookScraper()
    print("-" * 30)
    print(" Scraping Books.ToScrape.com")
    print("-" * 30)
    scraper.start_scraper(config)
    timer(start)


if __name__ == "__main__":
    main()
