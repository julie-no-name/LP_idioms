import requests
from bs4 import BeautifulSoup

from webapp.model import db, Idioms

def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def get_links_to_themes():
    html = get_html('https://www.native-english.ru/idioms/')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_idioms = soup.findAll('ul', class_="inlist inlist_loose")[1].findAll('li', class_="inlist__item")
        result_list_of_themes = []
        for idiom in all_idioms: 
            name_of_theme = (idiom.find('a').text).capitalize().strip()
            link_to_theme = 'https://www.native-english.ru' + idiom.find('a')['href']
            result_list_of_themes.append({
                'name_of_theme': name_of_theme,
                'link_to_theme': link_to_theme,
            })
        return result_list_of_themes
    return False

def get_python_idioms(theme, link):
    html = get_html(link)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_idioms = soup.find('ul', class_="list list_big").findAll('li', class_="list__item pane")
        result_idioms = []
        for idiom in all_idioms: 
            name_of_idiom = idiom.find('a').text
            translation = idiom.find('div', {'class': 'pane__text'}).text
            definition = idiom.find('div', {'class': 'example'}).text
            save_idioms(theme, name_of_idiom, translation, definition)
        return result_idioms
    return False


def save_idioms(name_of_theme, name_of_idiom, translation, definition):
    idioms_idioms = Idioms(name_of_theme=name_of_theme, name_of_idiom=name_of_idiom, translation=translation,definition=definition)
    db.session.add(idioms_idioms)
    db.session.commit()

