import requests
from bs4 import BeautifulSoup

class Html:
    html = None
    
    def __init__(self, url:str):
        self.url = url
        
    def get_url(self):
        return self.url
    
    def get_html(self):
        return self.html
    
    def get_html_text(self):
        return self.html.text
    
    def request(self):
        try:
            self.html = requests.get(self.url)
            if self.html.status_code == 200:
                print("Request dopadol uspesne!")
            else:
                print(f"Kod chyby: {self.html.status_code}")
        except:
            print("Zle zadana adresa")
    
class HtmlSearch():
    def __init__(self, html:Html):
        self.html = html
        self.soup = BeautifulSoup(html.get_html_text(), 'html.parser')
        
    def get_shop_links(self):
        links = []
        list_of_links = self.soup.find(id='left-category-shops')
        if list_of_links:
            for link in list_of_links.find_all('a'):
                links.append(link.get('href'))
            links = self.make_usable_link(links)
        return links
    
    def make_usable_link(self, links:list):
        base_url = self.html.get_url().removesuffix('/hypermarkte/')
        for i in range(len(links)):
             links[i] = base_url + links[i]
        return links
            