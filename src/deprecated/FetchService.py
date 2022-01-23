from urllib.parse import urljoin, urlsplit, urlunsplit
import requests
from bs4 import BeautifulSoup


def get_archive(url):
    link_list = []

    while url:
        r = requests.get(url)
        url_soup = BeautifulSoup(r.text, "html.parser")
        link_list.append(url)
        print(url)
        url = False

        for tag in url_soup.find_all('a', href=True):
            if tag.get("title") == "Weiter":
                next_page = tag.get("href")  # Doesn't find new link on last side, url=False stays and while-loop breaks
                url = urljoin("https://www.divi.de", next_page)
                print(url)
    return link_list


def generate_archive(url):
    counter = 0
    url = url.format(counter)
    while True:
        counter += 20
        yield (url)


def get_links(url, attribute):
    link_dict = {}
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup.find_all('a', href=True):
        if tag.get(attribute):
            link_dict[tag.get(attribute)] = tag.get("href")
    return link_dict


def merge_link_with_base(url, link):
    url = urlsplit(url)
    url = urlunsplit([url.scheme, url.netloc, link, None, None])  # Functions takes only iterable of 5
    return url



