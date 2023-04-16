import requests
from bs4 import BeautifulSoup
from string import punctuation
import os

ARTICLE_DATA = ('article', {'class': 'u-full-height c-card c-card--flush'})
SPAN_DATA = ('span', {'class': 'c-meta__type'})
A_DATA = ('a', {'class': 'c-card__link u-link-inherit'})
P_DATA = ('p', {'class': 'article__teaser'})


def get_file_name(link_text):
    link_text = ''.join(sign for sign in link_text if sign not in punctuation)
    return link_text.strip().replace(' ', '_') + '.txt'


def get_page_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    if p := soup.find(*P_DATA):
        return p.text
    return ''


def get_articles_text(url, articles_type):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all(*ARTICLE_DATA)
    files = []

    for article in articles:
        if article.find(*SPAN_DATA).text == articles_type:
            link = article.find(*A_DATA)
            href = 'https://www.nature.com' + link.get('href')
            file_name = get_file_name(link.text)
            files.append(file_name)

            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(get_page_text(href))


def main():
    page_count = int(input())
    articles_type = input()

    url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'

    for i in range(page_count):
        now_dir = f'Page_{i + 1}'
        os.mkdir(now_dir)
        os.chdir(now_dir)
        # print(os.getcwd())
        get_articles_text(f'{url}&page={i + 1}', articles_type)
        # print(os.listdir())
        os.chdir('..')
        # print()


if __name__ == "__main__":
    main()
