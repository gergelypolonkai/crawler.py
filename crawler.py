import urllib2
import sys
from bs4 import BeautifulSoup
import requests
import re

def make_url(link, base_url):
    if re.search(r'^[a-z-]+:', link):
        return link

    return re.sub(r'([^:])//+', r'\1/', base_url + '/' + link)

def main():
    checked_links = []
    link_cache = []

    if len(sys.argv) < 2:
        print("Usage: %s <url>" % sys.argv[0])
        return 1

        base_url = sys.argv[1]

        link_cache.append(base_url)

    while True:
        link = link_cache[0]
        link_cache = [x for x in link_cache if x != link]
        checked_links.append(link)

        print("Checking %s" % link)

        r = requests.get(link)

        if r.status_code == 200:
            soup = BeautifulSoup(r.content)

            for a in soup.find_all('a'):
                link = make_url(a.get('href'), base_url)

                if link.startswith(base_url):
                    if link not in checked_links:
                        link_cache.append(link)
                    else:
                        print("Skipping checked link %s" % link)
                else:
                    print("Skipping external link %s" % link)
        else:
            print r.status_code

        if len(link_cache) == 0:
            break

    print("Done. Checked links:")

    with open('link_list.txt', 'w') as f:
        for link in checked_links:
            f.write(link + "\n")
            print link

if __name__ == '__main__':
    main()
