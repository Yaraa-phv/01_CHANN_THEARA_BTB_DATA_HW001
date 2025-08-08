from bs4 import BeautifulSoup
import requests
import json
import re

url = 'https://www.womansday.com/relationships/dating-marriage/a41055149/best-pickup-lines/'
page = requests.get(url).text
soup = BeautifulSoup(page, 'html.parser')

info = {}

find_titles = soup.find_all('h2', title=True)

for h2 in find_titles:
    title = h2.text  
    ul = h2.find_next('ul')  
    
    if not ul:
        continue
    
    contents = ul.find_all('li')
    lines = []
    for li in contents:
        text = li.text.strip()

        # handle some of the unicode char ' 
        text = text.replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"').replace('\u2014', "'").replace('\u2018', "'")

        # remove unrelated content 
        if re.search(r'(RELATED:|ADVERTISEMENT)', text, re.IGNORECASE):
            continue

        # make sure it ends with a period
        if text and not text.endswith('.'):
            text += '.'

        lines.append(text)

    if lines:    
        info[title] = lines

with open('pickup_lines.json', 'w', encoding='utf-8') as file:
    json.dump(info, file, indent=2, ensure_ascii=True)
