import requests
from bs4 import BeautifulSoup


def tags_check(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    h1_tag = (soup.find('h1'))
    if h1_tag is not None:
        h1_tag = h1_tag.text
    title_tag = (soup.find('title'))
    if title_tag is not None:
        title_tag = title_tag.text
    meta_tag = (soup.find('meta', attrs={'name': 'description'}))
    if meta_tag is not None:
        meta_tag = meta_tag['content']
    print(meta_tag)
    return h1_tag, title_tag, meta_tag


if __name__ == '__main__':
    tags_check()
