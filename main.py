import json, datetime, re
import Search as search
import Write as write

SOURCE_URL = "https://www.prospektmaschine.de/hypermarkte/"

def main():
    source_html = search.Html(SOURCE_URL)
    source_html.request()
    
    html_search = search.HtmlSearch(source_html)
    
    links = html_search.get_shop_links()
    for l in links:
        print(l)
    #requestnut linky kazdeho obchodu / linku a z tamat vytiahnut info, prve ale preskumat html kod v prehiadaci
if __name__ == "__main__":
    main()



    