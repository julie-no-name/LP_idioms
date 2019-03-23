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

def get_python_idioms():
    html = get_html('https://www.native-english.ru/idioms/category/leg-and-foot/')
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
        html = get_html("https://www.native-english.ru/idioms/category/leg-and-foot/")
        if html:
            with open("idioms.html", "w", encoding="utf8") as f:
                f.write(html)
        idioms_list = get_python_idioms()
        with open('leg_and_foot.csv', 'w', encoding='utf-8', newline='') as user_file:
            fields = ['name_of_idiom', 'translation', 'definition']
            writer = csv.DictWriter(user_file, fields, delimiter=';')
            writer.writeheader()
            for idiom in idioms_list:
                writer.writerow(idiom)