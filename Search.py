import requests
import datetime as dt
from bs4 import BeautifulSoup

class Html:
    html = None
    
    def __init__(self, url:str):
        self.url = url
        
    def get_url(self):
        """Vráti url adresu stránky

        Returns:
            str: Reťazec url adresi
        """
        return self.url
    
    def get_html_text(self) -> str:
        """Vráti html kód ako text

        Returns:
            str: Reťazec html kódu
        """
        return self.html.text
    
    def request(self):
        """Získa html kód stránky
        """
        try:
            self.html = requests.get(self.url)
            if self.html.status_code != 200:
                print(f"Kod chyby: {self.html.status_code}")
        except Exception as e:
            print(f"Chyba pri requeste na stranku {self.url}: {e}")
    
class HtmlSearch():
    def __init__(self, html:Html):
        self.html = html
        self.soup = BeautifulSoup(html.get_html_text(), 'html.parser')
        
    def get_shop_links(self) -> list:
        """Vráti zozanam s všetkymi časťami linku pre podstrankz

        Returns:
            list: Zoznam s časťami linku pre podstránku
        """
        links = []
        list_of_links = self.soup.find(id='left-category-shops')
        if list_of_links:
            for link in list_of_links.find_all('a'):
                links.append(link.get('href'))
            links = self.make_usable_link(links)
        return links
    
    def make_usable_link(self, links:list) -> list:
        """Vráti zoznam použiteľných linkov pre podstránky

        Args:
            links (list): Zoznam s nekompletnými linkmi

        Returns:
            list: Zoznam použiteľných linkov
        """
        base_url = self.html.get_url().removesuffix('/hypermarkte/')
        for i in range(len(links)):
             links[i] = base_url + links[i]
        return links
    
    def get_prospekt(self) -> dict:
        """
        Vráti zoznam informacií o letákoch ako slovník
        Returns:
            list: ["tittle, thumbnail, shop_name, valid_from, valid_to, parsed_time"]
        """        
        letak_info = dict(tittle="", thumbnail="", shop_name="", valid_from="", valid_to="", parsed_time="")
        
        letaky_grid = self.soup.select_one('div.letaky-grid')
        brochure_div = letaky_grid.select('div.brochure-thumb')
        
        
        tittle_div = self.soup.select_one('div.current-section')
        letak_info["shop_name"] = tittle_div.select_one('span').text
        
        if brochure_div:
            for tag in brochure_div:
                date_info = tag.select_one('small').text
                dates = self.check_dates(date_info)
                if dates:
                    letak_info["valid_from"] = dates[0]
                    letak_info["valid_to"] = dates[1]
                else:
                    return None
                letak_info["tittle"] = tag.select_one('strong').text
                letak_info["thumbnail"] = tag.select_one('img').get('src')
                parse_info = dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                letak_info["parsed_time"] = parse_info
        else:
            return None
        return letak_info
    
    def check_dates(self, date_info:str) -> list:
        """Vráti informácie o platnosti len ak je leták aktuálny

        Args:
            date_info (str): Reťazec s informáciou platnosti

        Returns:
            list: [valid_from, valid_to]
        """
        try:
            dates = date_info.split(" - ")
            formated_dates = []
            for i in range(len(dates)):
                clean_date = dates[i].strip()
                date_obj = dt.datetime.strptime(clean_date, '%d.%m.%Y')
                if i == 0:
                    if date_obj.date() > dt.date.today():
                        return None
                else:
                    if date_obj.date() < dt.date.today():
                        return None
                formated_dates.append(date_obj.strftime('%Y-%m-%d'))
        except:
            return None
        return formated_dates
        
            