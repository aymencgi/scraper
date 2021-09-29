import requests
import csv
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/index.html"


def request_parser():
    request = requests.get(url)
    if request.ok:
        return BeautifulSoup(request.content, 'html.parser')


def category():
    category_link_short = []
    category_link = []
    for a in request_parser().select('li > a'):
        category_link.append("https://books.toscrape.com/" + a['href'])
        category_link_short.append(a['href'])
    category_link_short.pop(1)
    category_link.pop(1)
    category_link_short.pop(0)
    category_link.pop(0)
    category_link_short.pop()
    category_link.pop()
    return category_link_short, category_link


all_link_short_categories, all_link_categories = category()

#print(all_link_categories)


def pagitation():
    file = open("test.csv", "w")
    all_pagitation = []
    for link in all_link_categories:
        file.write(link + "\n")
        for numb in range(2, 10):
            all_pages = link.replace("index.html", f'page-{numb}.html')
            request = requests.get(all_pages)
            if not request.ok:
                break
            file.write(all_pages + "\n")
            all_pagitation.append(all_pages)
    file.close()
    return all_pagitation


extra_pages = pagitation()

categories_with_pagitation = all_link_categories + extra_pages

#print(categories_with_pagitation)

urlpage = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
souptest = BeautifulSoup(urlpage, "html.parser")
booktest = souptest.findAll("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})

def pages():
    book_links = []
    for page in categories_with_pagitation:
        r = requests.get(page)
        soup = BeautifulSoup(r.content, 'html.parser')
        for w in soup.select('h3 > a'):
            x = w['href']
            u = "https://books.toscrape.com/catalogue/" + x.replace('../', '')
            # print(u)
            book_links.append(u)
    return book_links



all_books = pages()
#print(all_books)

categories_name = ["Travel", "Mystery"]



headers = ["Title","UPC","Price including tax","Price excluding tax","Avaibility","product Description","Tax","book_category","review_rating","image_url"]
def book_data():
    for categories in categories_name:
        with open(f'{categories}.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            row = []
            books = []
            for book in all_books:
                request = requests.get(book)
                soup = BeautifulSoup(request.content, 'html.parser')
                title = soup.find("h1").text
                row.append(title)

                # UPC code
                UPC_code = soup.find_all("td")[0].text
                row.append(UPC_code)

                # Price including tax
                price_including_tax = soup.find_all("td")[3].text
                row.append(price_including_tax)

                # Price excluding tax
                price_excluding_tax = soup.find_all("td")[2].text
                row.append(price_excluding_tax)

                # Number available
                number_available = soup.find_all("td")[5].text
                row.append(number_available)

                # product Description
                product_description = soup.find_all("p")[3].text
                row.append(product_description)

                # Category
                book_category = soup.select('li > a')
                row.append(book_category[2].text)

                # Review rating
                review_rating = soup.find_all("p", class_="star-rating")[0].get("class")[1]
                if review_rating:
                    row.append(review_rating)
                else:
                    row.append("No star review")
                # Getting Image URL

                image_url = soup.find('div', class_="item active").img['src']
                image_url = "http://books.toscrape.com/" + image_url.replace('../', '')
                row.append(image_url)
                print("book title",title)
                # print("livres")
                # print(book)
            books.append(row)
            writer.writerows(books)

book_data()

# CRRER UNE FONCTIONS QUI RECUPER DES LIVRES D4UNE CATEGORIE TOUTES LES DONNEES
# CREER LE DEPOT GITHUB ET METTRE LE CODE





