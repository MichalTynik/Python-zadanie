import requests, bs4, json, datetime, re

class HttpRequest:
    def __init__(self, address):
        self.address = address

    def getUrl(self):
        return self.address
    
    def getHtml(self):
        req = requests.get(self.address)
        return req.text

def main():
    try:
        url = input(str("Zada URL stranky: ")) #https://www.prospektmaschine.de/hypermarkte/
    except:
        print("Toto nie je string")
    httpReq = HttpRequest(url)
    htmlCode = httpReq.getHtml()
    with open("html.txt", "w") as file:
        file.write(htmlCode)
    # hladat podla id: left-category-shops

if __name__ == "__main__":
    main()



    