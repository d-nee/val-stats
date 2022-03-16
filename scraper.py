import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from html.parser import HTMLParser
from urllib.parse import urljoin

CHROMEDRIVER_PATH = './chromedriver.exe'

STAT_KEYS = ['ACS', 'K', 'D', 'A', 'KD-DIFF', 'K/D',
        'ADR', 'HSP', 'FK', 'FD', 'MK', 'ECON']

class PlayerHTMLParser(HTMLParser):
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
    parser = PlayerHTMLParser()
    if content is not None:
        parser.urls = []
        parser.feed(content)
        parser.close()
        links = parser.get_links()
    return links


def get_driver():
    options = Options()
    # options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    s = webdriver.chrome.service.Service(CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=s, options=options) 


def get_profile_html(name, discrim):
    # They put a cloudflare blocker the day after I wrote this

    # url = 'https://tracker.gg/valorant/profile/riot/' + \
    #       {name.replace(' ', '%20')} + f'%23{discrim}' + \
    #        '/matches?playlist=competitive&season=all'
    # driver = get_driver()
    # driver.get(url)
    # time.sleep(5)
    # js = 'document.getElementsByTagName(\"button\")[1].click();'
    # while True:
    #     try:
    #         driver.find_element(by=By.XPATH, 
    #             value='//*[contains(text(), \"Load More Matches\")]').click()
    #         time.sleep(5)
    #     except:
    #         break
    # content = driver.page_source
    # driver.close()

    # Manual downloads:
    with open(f'./html/{name}_{discrim}.html') as file:
        content = file.read()
    return content

def get_match_html(gamehash):
    url = f'https://tracker.gg/valorant/match/{gamehash}'
    driver = get_driver()
    driver.get(url)
    time.sleep(3)
    content = driver.page_source
    driver.find_element(by=By.XPATH, 
        value='//*[contains(text(), \"Duels\")]').click()
    time.sleep(3)
    agent_content = driver.page_source
    driver.close()
    return content, agent_content


def get_agents(agent_content):
    pid_agents = dict()
    soup = BeautifulSoup(agent_content, 'html.parser')
    names_raw = soup.find_all('span', {'class':'trn-ign'})
    agents_raw = soup.find_all('div', {'class':'player-info__agent'})
    for i in range(10):
        pid_agents[names_raw[i].text[:-1]] = agents_raw[i].text
    return pid_agents


def handle_match_rows(row):
    entries = row.find_all('td')
    pid = entries[0].find('span', {'class':'trn-ign'}).text[:-1]
    rank = entries[1].find('img').get('title')
    p_dict = dict()
    p_dict['rank'] = rank
    for i, e in enumerate(STAT_KEYS):
        p_dict[e] = entries[i+2].text
        # Remove % symbol for HSP
        if e == 'HSP':
            p_dict[e] = p_dict[e][:-1]
    return pid, p_dict


# Get all stats of players in a match
def get_match_player_info(gamehash, pid_agents, soup):
    tables = soup.find_all('tbody')
    players = []
    for i, e in enumerate(['A', 'B']):
        rows = tables[i].find_all('tr')
        for r in rows:
            pid, p_dict = handle_match_rows(r)
            pid_comp = pid.split('#')
            p_dict['gamehash'] = gamehash
            p_dict['name'] = pid_comp[0].lower()
            p_dict['discrim'] = pid_comp[1]
            p_dict['team'] = e
            p_dict['agent'] = pid_agents[pid]
            players.append(p_dict)
    return players


def match_dict(gamehash, match_map, start_dt, duration, scores, a_econ, b_econ):
    m_dict = dict()
    m_dict['gamehash'] = gamehash
    m_dict['map'] = match_map
    start_d = start_dt[0].split('/')
    if start_dt[1][-2:] == 'PM':
        start_time = f'{int(start_dt[1][0:2])+12}{start_dt[1][2:5]}'
    else:
        start_time = start_dt[1][0:5]
    sql_dt = f'20{start_d[2]}-{start_d[0]}-{start_d[1]} {start_time}:00'
    m_dict['start_time'] = sql_dt
    dur_str = ''
    for time_unit in ['h', 'm', 's']:
        if time_unit in duration:
            d_split = duration.split(time_unit)
            amt = d_split[0].rjust(2, '0')
            dur_str += amt + ':'
            duration = d_split[1]
        else:
            dur_str += '00:'
    m_dict['duration'] = dur_str[:-1]
    m_dict['a_score'] = scores[0]
    m_dict['b_score'] = scores[1]
    m_dict['a_bank'] = a_econ[0].replace(',', '')
    m_dict['a_loadout'] = a_econ[1].replace(',', '')
    m_dict['b_bank'] = b_econ[0].replace(',', '')
    m_dict['b_loadout'] = b_econ[1].replace(',', '')
    return m_dict


# Get all gamehashes played by a given player
def get_player_gamehashes(name, discrim):
    content = get_profile_html(name, discrim)
    links = fetch_links(content)
    return [x.split('match/')[1] for x in links if '/match/' in x]


# Get all match info given match hash
def get_match_info(gamehash):
    content, agent_content = get_match_html(gamehash)
    soup = BeautifulSoup(content, 'html.parser')
    match_map = soup.find('span', {'class':'metadata__playlist-map'}).text
    scores = [s.text for s in soup.find_all('span', {'class':'team__value'})]
    duration = soup.find('span', {'class':'metadata__time-duration'}).text
    duration = duration.replace(' ', '')
    start_dt = soup.find('span', {'class':'metadata__time-timestamp'}).text
    start_dt = start_dt.replace(' ', '').split(',')
    a_econ = [s.text for s in soup.find_all('span', {'class':'value--team-0'})]
    b_econ = [s.text for s in soup.find_all('span', {'class':'value--team-1'})]
    m_dict = match_dict(gamehash, match_map, start_dt, duration, scores,
                        a_econ, b_econ)
    pid_agents = get_agents(agent_content)
    p_dicts = get_match_player_info(gamehash, pid_agents, soup)
    return m_dict, p_dicts
