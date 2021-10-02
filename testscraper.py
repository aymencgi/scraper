import requests
import csv
from bs4 import BeautifulSoup

#fonction qui request l'URL de base

def request_parser(url):
    url = "https://books.toscrape.com/index.html"
    request = requests.get(url)
    if request.ok:
        return BeautifulSoup(request.content, 'html.parser')



#fonction qui renvoie les liens des catégories
def category():
    url = "https://books.toscrape.com/index.html"
    category_link_short = []
    category_link = []
    for a in request_parser(url).select('li > a'):
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


#fonction qui recherche les noms des catégories et les mets dans une liste
category_name = []
for category in request_parser(category).select('li > a'):
    category_name.append(category.text)
print(category_name)


#fonction qui scan les liens des catégories, fait la pagination et retour tout les liens des livres

def onecategorybooks(categoryUrl):
    books_of_category = []
    url = categoryUrl
    links = []
    r = requests.get(url)
    r_url = BeautifulSoup(r.content, 'html.parser')
    for w in r_url.select('h3 > a'):
        x = w['href']
        c = "https://books.toscrape.com/catalogue/" + x.replace('../', '')
        links.append(c)
    for numb in range(2, 10):
        all_pages = url.replace("index.html", f'page-{numb}.html')
        request = requests.get(all_pages)
        if not request.ok:
            break
        books_of_category.append(url)
        books_of_category.append(all_pages)
        soup = BeautifulSoup(request.content, 'html.parser')
        for w in soup.select('h3 > a'):
            x = w['href']
            u = "https://books.toscrape.com/catalogue/" + x.replace('../', '')
            links.append(u)
        return links




headers = ["Title", "UPC", "Price including tax", "Price excluding tax", "Avaibility", "product Description", "Tax",
           "book_category", "review_rating", "image_url"]
categories_name = ["Travel", "Mystery","Historical Fiction","Sequential Art","Classics","Philosophy","Romance","Womens Fiction","Fiction","Childrens","Religion","Nonfiction",
                   "Music","Default","Science Fiction","Sports and Games","Add a comment","Fantasy","New Adult","Young Adult","Science","Poetry","Paranormal","Art","Psychology",
                   "Autobiography","Parenting","Adult Fiction","Humor","Horror","History","Food and Drink","Christian Fiction","Business","Biography","Thriller","Contemporary",
                   "Spirituality","Academic","Self Help","Historical","Christian","Suspense","Short Stories","Novels","Health","Politics","Cultural","Erotica","Crime"
                   ]

#fonction qui crée un fichier pour chaque catégorie et qui enregistre les headers et  toutes les données de toutes les livres sans prendre en compte la catégorie

def bokkdata():
    for categories in categories_name:
        with open(f'{categories}.csv', 'w', encoding='utf-8') as filename:
            writer = csv.writer(filename)
            writer.writerow(headers)
            rows = []
            for link in all_link_categories:
                row = []
                request = requests.get(link)
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
                print("book title", title)
                rows.append(row)
                # print("livres")
            writer.writerows(rows)
