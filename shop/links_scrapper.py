import logging
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from queue import Queue

import requests
from bs4 import BeautifulSoup


TIME_OUT = 10

LOCK = Lock()

logger = logging.getLogger('logit')


def links_worker(queue: Queue):
    while True:
        url = queue.get()
        logger.debug(f'[WORKING ON] {url}')
        try:
            with requests.Session() as session:
                response = session.get(
                    url,
                    allow_redirects=True,
                    timeout=TIME_OUT
                )
                logger.debug(response.status_code)

                if response.status_code == 404:
                    logger.warning(f'Page not found {url}')
                    break

                assert response.status_code in (200, 301, 302), 'Bad response'

            soup = BeautifulSoup(response.text, 'html.parser')
            # Getting product links
            links = soup.select('#collection-grid a')
            links = '\n'.join([
                f"https://no6store.com{link.get('href')}" for link in links
            ])
            with LOCK:
                with open('links.txt', 'a') as file:
                    file.write(links)

        except (
            requests.Timeout,
            requests.TooManyRedirects,
            requests.ConnectionError,
            requests.RequestException,
            requests.ConnectTimeout,
            AssertionError
        ) as error:
            logger.error(f'An error happen {error}')
            queue.put(url)

        if queue.qsize() == 0:
            break


def main():
    category_urls = [
        'https://no6store.com/collections/clothing-sweaters',
        'https://no6store.com/collections/shoes-no-6-boots',
        'https://no6store.com/collections/shoes-all',
        'https://no6store.com/collections/shoes-footwear',
        'https://no6store.com/collections/shoes-no-6-clogs',
        'https://no6store.com/collections/shoes-all-no-6-footwear',
        'https://no6store.com/collections/clothing-dresses',
        'https://no6store.com/collections/accessories-bags',
        'https://no6store.com/collections/clothing-tops',
        'https://no6store.com/collections/clothing-sweaters',
        'https://no6store.com/collections/clothing-skirts',
        'https://no6store.com/collections/clothing-shorts-and-pants',
        'https://no6store.com/collections/clothing-jumpsuits',
        'https://no6store.com/collections/accessories-hats',
        'https://no6store.com/collections/accessories-jewelry',
        'https://no6store.com/collections/accessories-socks-and-tights',
        'https://no6store.com/collections/clothing-swimwear',
        'https://no6store.com/collections/clothing-lingerie-and-intimates',
        'https://no6store.com/collections/clothing-jackets-and-outerwear',
        'https://no6store.com/collections/accessories-all',
        'https://no6store.com/collections/clothing-all',
        'https://no6store.com/collections/belts',
        'https://no6store.com/collections/shearling-boots',
        'https://no6store.com/collections/sunglasses',
        'https://no6store.com/collections/flat-base-clogs',
        'https://no6store.com/collections/accessories-scarves-gloves',
        'https://no6store.com/collections/clog-sandals-and-shoes',
        'https://no6store.com/collections/clogs-clog-boots',
        'https://no6store.com/collections/socksss',
    ]

    queue = Queue()

    for url in category_urls:
        queue.put(url)

    worker_number = 20

    with ThreadPoolExecutor(max_workers=worker_number) as executor:
        for _ in range(worker_number):
            executor.submit(links_worker, queue)


if __name__ == '__main__':
    main()
