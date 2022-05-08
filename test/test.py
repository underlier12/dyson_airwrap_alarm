from bs4 import BeautifulSoup

with open('test.html', encoding='utf-8') as html:
    soup = BeautifulSoup(html, 'html.parser')
    button = soup.find('button', {'class': 'card__addtocart'})
    print(button.span.text)
