from web_scraper import start_scrape
from urllib.request import urlopen, Request

def main():
    
    webpage = input("Cole o link para fazer webscraping de emails: ")

    try:
        page = urlopen(webpage) 
        start_scrape(page)
    except:
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(webpage, headers=hdr)
        page = urlopen(req)
        start_scrape(page)

if __name__ == "__main__":
    main()