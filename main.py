import time

from scraper import BookScraper


def timer(start_time):
    end_time = int(time.time()) - start_time
    mins = end_time // 60
    secs = end_time % 60
    end_time = '{:02d} mins {:02d} secs.'.format(mins, secs)
    print('\n\nAll books exported in ' + end_time)


if __name__ == "__main__":
    start_time = int(time.time())

    scraper = BookScraper()
    scraper.start_scraper()

    timer(start_time)
