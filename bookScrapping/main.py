#importing required libraries
from bs4 import BeautifulSoup
import requests
import psycopg2


#connecting to the database. change the fields as per requirements
connection = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                password="django123",
                port="5432")

cursor = connection.cursor()

#creating a table in the database
cursor.execute("create table Books (id int, Name VARCHAR(50), Price VARCHAR(5), Availability VARCHAR(20), Ratings_out_of_5 int);")

connection.commit()
rating_convertor = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}

#inserting books data into the table created.
for i in range(1, 51):
    url = f'http://books.toscrape.com/catalogue/page-{i}.html'
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'lxml')
    books = soup.find_all('article', class_='product_pod')
    for book in books:
        name = book.h3.a['title']
        prod_info = book.find('div', class_='product_price')
        price = prod_info.find('p', class_='price_color').text
        availability = prod_info.find('p', class_='instock availability').text.strip()
        ratings = rating_convertor[book.p['class'][1]]

        cursor.execute(f'INSERT INTO Books(Name, Price, Availability, Ratings_out_of_5) VALUES( {name}, {price}, {availability}, {ratings});')


connection.commit()

#closing the cursor and connection
cursor.close()
connection.close()
