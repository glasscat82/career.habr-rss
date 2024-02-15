""" parse //career.habr.com/vacancies/rss """
import sys
from datetime import datetime as dt
import requests, fake_useragent
from bs4 import BeautifulSoup
from art import tprint

def p(text, *args):
    print(text, *args, sep=' / ', end='\n')

def get_html(url_page):
    header = { 'User-Agent':str(fake_useragent.UserAgent().google), }

    try:
        page = requests.get(url=url_page, headers = header, timeout = 10)
        return page.text

    except Exception as e:
        print(sys.exc_info()[1])
        return False

def get_all_links(html):
    """ links is url """
    if html is False:
        False

    soup = BeautifulSoup(html, 'lxml')
    selection_list = soup.find('channel')

    links = []
    for item in selection_list.find_all('item'):
        
        res = {}
        for key, tg in enumerate(item.children, 0):
            n = tg.name
            t = tg.text.strip()

            if len(t) > 0:
                if n == None:
                    n = 'url'
                
                if n == 'pubdate':
                    t = dt.strptime(t, '%a, %d %b %Y %H:%M:%S %z')

                res[f'{n}'] = t
        
        links.append(res)
    
    return links

if __name__ == "__main__":
    
    start = dt.now()
    #---------------start
    print('\033[36m')
    tprint('.:: career.habr .::. rss ::.', font='cybermedium', sep='\033[0m\n')
    url = 'https://career.habr.com/vacancies/rss?currency=RUR&sort=relevance&type=all'
    l = get_all_links(get_html(url))

    for v in l:
        p(f"\033[32m{v['pubdate'].strftime('%d.%m.%y %I:%M')} {v['title']}\033[0m")
        p(f"\033[33m{v['description']}\033[0m")
        p(f"\033[35m{v['url']}\033[0m")
    #--------------quit
    end = dt.now()
    print(f'\033[36m[+] lead time {str(end-start)}\033[0m', end='\n')