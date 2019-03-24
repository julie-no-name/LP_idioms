import requests
import csv
from bs4 import BeautifulSoup

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
            name_of_csv = name_of_theme.lower().replace(' ', '_') + '.csv'
            result_list_of_themes.append({
                'name_of_theme': name_of_theme,
                'link_to_theme': link_to_theme,
                'name_of_csv': name_of_csv
            })
        return result_list_of_themes
    return False

def get_python_idioms(link):
    html = get_html(link)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_idioms = soup.find('ul', class_="list list_big").findAll('li', class_="list__item pane")
        result_idioms = []
        for idiom in all_idioms: 
            name_of_idiom = idiom.find('a').text
            translation = idiom.find('div', {'class': 'pane__text'}).text
            definition = idiom.find('div', {'class': 'example'}).text
            result_idioms.append({
                'name_of_idiom': name_of_idiom.strip(),
                'translation': translation.strip(),
                'definition': definition.strip()
            })
        return result_idioms
    return False

if __name__ == "__main__":
        list_of_themes = get_links_to_themes()
        for theme in list_of_themes:
            idioms_list = get_python_idioms(theme['link_to_theme'])
            with open(theme['name_of_csv'], 'w', encoding='utf-8', newline='') as user_file:
                fields = ['name_of_idiom', 'translation', 'definition']
                writer = csv.DictWriter(user_file, fields, delimiter=';')
                writer.writeheader()
                for idiom in idioms_list:
                    writer.writerow(idiom)