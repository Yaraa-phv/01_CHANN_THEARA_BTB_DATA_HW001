from bs4 import BeautifulSoup
import requests
import json

url = 'https://www.womansday.com/relationships/dating-marriage/a41055149/best-pickup-lines/'
page = requests.get(url).text
soup = BeautifulSoup(page, 'html.parser')

info = {}

# Find all title with h2 
find_titles = soup.find_all('h2', title=True)

for h2 in find_titles:
    title = h2.text  
    # To find the first ul that next to h2
    ul = h2.find_next('ul')  
    
    # If not found, just contiue to another h2
    # if not ul:
    #     print(f"There is a none of ul in h2 : {h2}")
    #     continue
    
    # find all li in ul
    contents = ul.find_all('li')
    lines = []
    for li in contents:
        pickup_lines = li.text
        lines.append(pickup_lines)
    
    info[title] = lines

with open('pickup_lines.json', 'w', encoding='utf-8') as file:
    json.dump(info, file, indent=2)
