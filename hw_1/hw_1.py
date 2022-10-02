import sys
import requests, requests.exceptions, re, os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import shutil

if os.path.exists('data'):
    shutil.rmtree(f'{os.getcwd()}/data/')
os.mkdir('data')

all_links, n = {}, 0

def web_crawler(url, depth):
    global all_links, n
    depth = int(depth)
    try:
        resp = requests.get(f'{url}')
        soup = BeautifulSoup(resp.text, 'html.parser')
        if not resp.ok or str(resp.status_code)[0] in ['4', '5']:
            return

        if depth >= 0:
            for i in soup.findAll('a', attrs={'href': re.compile("http.")}):
                link = i.get('href')
                if urlparse(link).netloc.split('.')[-2] == urlparse(url).netloc.split('.')[-2] and link not in all_links.values():
                    site = requests.get(f'{link}')
                    if str(site.status_code)[0] in ['4', '5']:
                        break
                    n += 1
                    all_links.update({n: link})
                    if n == 1 and os.path.exists('links.txt'):
                        os.remove('links.txt')
                    with open('links.txt', 'a') as links:
                        links.write(f'{n} {link}\n')
                    with open(f'data/{n}.html', 'w') as file:
                        file.write(site.text)
                    web_crawler(link, depth - 1)
        else:
            if url not in all_links.values():
                n += 1
                all_links.update({n: url})
                if n == 1 and os.path.exists('links.txt'):
                        os.remove('links.txt')
                with open('links.txt', 'a') as links:
                    links.write(f'{n} {url}\n')
                with open(f'data/{n}.html', 'w') as file:
                    file.write(resp.text)
    except requests.exceptions.MissingSchema:
        url = input('Введите корректный url (в формате https://...): ')
        web_crawler(url, depth)
    except requests.exceptions.ConnectionError:
        print('Ошибка подключения. Попробуйте заново')
        return
    except TypeError:
        depth = int(input('Введите корректную глубину поиска (в виде целого числа): '))
        web_crawler(url, depth)

if __name__ == '__main__':
    web_crawler(sys.argv[1], sys.argv[2])
