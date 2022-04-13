#importing necessary libraries
import requests
import psycopg2

#making connection with the database
connection = psycopg2.connect(
                host="localhost",
                database="tailnode",
                user="postgres",
                password="django123",
                port="5432")

cursor = connection.cursor()

#creating the users table in the database
cursor.execute('CREATE TABLE Users (User_id VARCHAR(30), Title VARCHAR(10), Firstname VARCHAR(50), Lastname VARCHAR(50), Picture_link VARCHAR(100));')
connection.commit()
response = requests.get('https://dummyapi.io/data/v1/user', headers={'app-id': '62568ae89312b5a8218a8b53'})

#inserting the users data in the table created
users = response.json()['data']
for user in users:
    user_id = user['id']
    title = user['title']
    firstname = user['firstName']
    lastname = user['lastName']
    picture_link = user['picture']

    cursor.execute(f'INSERT INTO users( User_id, Title, Firstname, Lastname, Picture_link) VALUES({user_id}, {title}, {firstname}, {lastname}, {picture_link});')
    connection.commit()

#creating a new table for posts
cursor.execute(f'CREATE TABLE posts (Post_id VARCHAR(30), Image VARCHAR(50), Likes int, Tags VARCHAR, Caption VARCHAR, Publish_date VARCHAR, owner VARCHAR);')

#inserting the posts data in the posts table
user_ids = cursor.execute('select User_id from users')
for user_id in user_ids:
    res = requests.get(f'https://dummyapi.io/data/v1/user/{user_id}/post', headers={'app-id': '62568ae89312b5a8218a8b53'})
    posts = res.json()['data']
    for post in posts:
        post_id = post['id']
        image = post['image']
        likes = post['likes']
        tags = post['tags']
        caption = post['text']
        publishDate = post['publishDate']
        owner = post['firstName'] + ' ' + post['lastName']

        cursor.execute(f'INSERT INTO posts(Post_id, Image, Likes, Tags, Caption, Publish_date, Owner) VALUES({post_id}, {image}, {likes}, {tags}, {caption}, {publishDate}, {owner});')
        connection.commit()


#closing the connection
cursor.close()
connection.close()