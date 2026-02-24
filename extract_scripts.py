from bs4 import BeautifulSoup
import re

with open('temp_doc.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
scripts = soup.find_all('script')
for script in scripts:
    if script.get('src'):
        print(script['src'])
