
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from html.parser import HTMLParser
from urllib.parse import urljoin

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a' or tag == 'area': # extract href links
            href = [v for (k, v) in attrs if k == 'href']
            self.urls.extend(href)
        if tag == 'frame' or tag == 'iframe': # extra src links
            src = [v for (k, v) in attrs if k == 'src']
            self.urls.extend(src)

    # Refine the hyperlinks: ignore the parameters in dynamic URLs, convert
    # all hyperlinks to absolute URLs, and remove duplicated URLs.
    def get_links(self):
        res = set()       # use a set to avoid duplicated URLs
        for url in self.urls:
            url = url.split('?')[0]   # extract the part before '?' if any
            url = url.split('#')[0]   # extract the part before '#' if any
            url = urljoin('https://tracker.gg', url.strip())   # absolute URL
            res.add(url)
        return list(res)

def fetch_links(content):
    links = None
    parser = MyHTMLParser()
    if content is not None:
        parser.urls = []
        parser.feed(content)
        parser.close()
        links = parser.get_links()
    return links

def get_match_html(name, discrim):
    url = f'https://tracker.gg/valorant/profile/riot/{name}%23{discrim}' + \
           '/matches?playlist=competitive&season=all'
    s = webdriver.chrome.service.Service('./chromedriver.exe')
    driver = webdriver.Chrome(service=s) 
    
    driver.get(url)
    time.sleep(5)
    js = 'document.getElementsByTagName(\"button\")[1].click();'
    while True:
        try:
            driver.find_element(by=By.XPATH, 
                value="//*[contains(text(), 'Load More Matches')]").click()
            time.sleep(5)
        except:
            break
    content = driver.page_source
    driver.close()
    
    return content

def get_match_hashes(name, discrim):
    content = get_match_html(name, discrim)
    links = fetch_links(content)
    return [x.split('match/')[1] for x in links if '/match/' in x]

print(get_match_hashes("Synesthesiac", "1881"))
print(get_match_hashes("amypham2", "5006"))