from concurrent.futures import ThreadPoolExecutor
from queue import Queue

import requests
from bs4 import BeautifulSoup

from shop.models import Category


TIME_OUT = 10


def worker(queue: Queue):
    while True:
        url, category = queue.get()
        print('[WORKING ON]', url)
        try:
            with requests.Session() as session:
                response = session.get(
                    url,
                    allow_redirects=True,
                    timeout=TIME_OUT
                )
                print(response.status_code)

                if response.status_code == 404:
                    print('Page not found', url)
                    break

                assert response.status_code in (200, 301, 302), 'Bad response'

            soup = BeautifulSoup(response.text, 'html.parser')
            images = soup.select('a div img')
            if images:
                image_url = images[0].get('src')
                with requests.Session() as session:
                    img_response = session.get(image_url, timeout=TIME_OUT)
                image_name = f'{category.name}.jpg'
                with open(f'media/category/images/{image_name}', 'wb') as file:
                    file.write(img_response.content)

                category.image = f'category/images/{image_name}'
                category.save()
                print('DONE!!!')

        except (
            requests.Timeout,
            requests.TooManyRedirects,
            requests.ConnectionError,
            requests.RequestException,
            requests.ConnectTimeout,
            AssertionError
        ) as error:
            print('An error happen', error)
            queue.put(url)

        if queue.qsize() == 0:
            break


def main():
    categories = Category.objects.exclude(name='all')

    queue = Queue()
    url = 'https://www.google.com/search?um=1&hl=en&safe=active&nfpr=1&q={name}&start=1&tbm=isch'
    for category in categories:
        queue.put((url.format(name=category.name), category))

    worker_number = 5

    with ThreadPoolExecutor(max_workers=worker_number) as executor:
        for _ in range(worker_number):
            executor.submit(worker, queue)


if __name__ == '__main__':
    main()
