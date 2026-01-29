import Search as search
import Write as write

SOURCE_URL = "https://www.prospektmaschine.de/hypermarkte/"

def main():
    source_html = search.Html(SOURCE_URL)
    source_html.request()
    
    html_search = search.HtmlSearch(source_html)
    
    links = html_search.get_shop_links()
    
    info = []
    
    for sub_link in links:
        sub_html = search.Html(sub_link)
        sub_html.request()
        sub_html_search = search.HtmlSearch(sub_html)
        info_temp = sub_html_search.get_prospekt()
        if info_temp:
            info.append(info_temp)

    save = write.Data("data.json")
    save.save_info(info)
        
        
        
if __name__ == "__main__":
    main()



    