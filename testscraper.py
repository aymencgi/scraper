import requests
import csv
from bs4 import BeautifulSoup
import os


# fonction qui request l'URL de base

def request_parser(url):
    #url = "https://books.toscrape.com/index.html"
    request = requests.get(url)
    if request.ok:
        return BeautifulSoup(request.content, 'html.parser')


headers = ["Title", "UPC", "Price including tax", "Price excluding tax", "Avaibility", "product Description", "Tax",
               "book_category", "review_rating", "image_url"]
categories_name = ["Travel", "Mystery", "Historical Fiction", "Sequential Art", "Classics", "Philosophy", "Romance",
                       "Womens Fiction", "Fiction", "Childrens", "Religion", "Nonfiction",
                       "Music", "Default", "Science Fiction", "Sports and Games", "Add a comment", "Fantasy",
                       "New Adult", "Young Adult", "Science", "Poetry", "Paranormal", "Art", "Psychology",
                       "Autobiography", "Parenting", "Adult Fiction", "Humor", "Horror", "History", "Food and Drink",
                       "Christian Fiction", "Business", "Biography", "Thriller", "Contemporary",
                       "Spirituality", "Academic", "Self Help", "Historical", "Christian", "Suspense", "Short Stories",
                       "Novels", "Health", "Politics", "Cultural", "Erotica", "Crime"
                       ]



# fonction qui renvoie les liens des catégories
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

# print(all_link_categories)


# fonction qui scan les liens des catégories, fait la pagination et retour tout les liens des livres



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

pages = []

#print(pages[0][0])

def get_book_bycategory():
    for category in all_link_categories:
        pages.append(onecategorybooks(category))
    for category in categories_name:
        if not os.path.exists("category"):
            os.makedirs(category)


    for index, row in enumerate(pages):
        path = os.getcwd()
        with open(os.path.join(path, "{}.csv".format(categories_name[index]), "w", newline="") as f:
        #with open("{}.csv".format(categories_name[index]), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            rows = []
            for link in pages[index]:
                page_soup = request_parser(link)
                #print(page_soup)
                bookshelf = page_soup.find_all("td")
                title = page_soup.find("h1").text
                new_list = [x.text for x in bookshelf]
                new_list.insert(0, title)
                review_rating = page_soup.find_all("p", class_="star-rating")[0].get("class")[1]
                if review_rating:
                    new_list.append(review_rating)
                else:
                    new_list.append("No star review")

                image_url = page_soup.find('div', class_="item active").img['src']
                image_url = "http://books.toscrape.com/" + image_url.replace('../', '')
                new_list.append(image_url)
                rows.append(new_list)
            writer.writerows(rows)

get_book_bycategory()


def get_images():
    all_title = []
    all_images = []
    for index, row in enumerate(pages):
        for link in pages[index]:
            page_soup = request_parser(link)
            title = page_soup.find("h1").text
            image_url = page_soup.find('div', class_="item active").img['src']
            image_url = "http://books.toscrape.com/" + image_url.replace('../', '')
            all_images.append(image_url)
            all_title.append(title)
            os.mkdir(os.path.join(os.getcwd(),images))
            with open(os.path.join(f'{title}.jpg'),'ab') as file:
                for image in all_images:
                    r = requests.get(image).content
                file.write(r)


get_images()


