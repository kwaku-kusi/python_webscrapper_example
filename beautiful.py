import re
import requests
from bs4 import BeautifulSoup

def in_stock(title, topic):
    title = title.strip()
    url = "http://books.toscrape.com/"
    
    web_page = requests.get(url)
    soup = BeautifulSoup(web_page.text, "html.parser")
    
    cat = soup.find("aside").find("ul").find("ul").find_all("li")
    found_cat = False
    cat_url = ""
    
    for li in cat:
        txt = li.text.strip()
        
        if topic.lower() == txt.lower():
            found_cat = True
            cat_url = li.find('a')["href"]

        
    
    if not found_cat:
        return False
    
    extra = ""
    url += cat_url 
    book_available = False

    while True:

        if extra != "":
            url = str(url)
            cram = url.rsplit('/',1)
            url = f"{cram[0]}/{extra}"
        
        
        web_page = requests.get(url)
        soup = BeautifulSoup(web_page.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")
        

        for book in books:
            
            book_title = book.find("h3").find("a")["title"]
            print(book_title,"\n", title,"\n\n")

            if re.search(title, book_title, re.IGNORECASE) or book_title == title:
                return True
                stock_qty = book.find("div", class_="product_price").find("p", class_="instock availability")
                stock_txt = stock_qty.text.strip()

                if re.search(stock_txt, "in stock", re.IGNORECASE):
                    book_available = True
                    break
        
        try:
            next_btn = soup.find("ul", class_="pager").find("li", class_="next")
            if next_btn == None: break
        except:
            break
        
        extra = next_btn.find("a")["href"]

    


    return book_available
        


if __name__ == "__main__":
    p = in_stock("While You Were Mine","Historical Fiction")
    # p = in_stock("Online Marketing for Busy Authors: A Step-By-Step guide", "self help")
    # p = in_stock("the selfish gene","science")
    # p = in_stock("The Murder of Roger Ackroyd (Hercule Poirot #4)", "mystery")
    print(p)