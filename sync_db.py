from modules import *


(cnx, cursor) = create_connection()

sql = """CREATE TABLE categories
        (
        id serial,
        name varchar(80),
        description varchar(255),
        PRIMARY KEY(id)
        );"""
cursor.execute(sql)

sql = """CREATE TABLE expenses
        (
        id serial,
        category_id int,
        name varchar(120),
        expense decimal(7, 2),
        date date,
        PRIMARY KEY(id),
        FOREIGN KEY(category_id) REFERENCES categories(id) ON DELETE CASCADE
        );"""
cursor.execute(sql)

sql = """INSERT INTO categories(name, description) 
        VALUES('Rachunki', 'wszelkiego typu opłaty');"""
cursor.execute(sql)

sql = """INSERT INTO categories(name, description) 
        VALUES('Żywność', 'jedzenie');"""
cursor.execute(sql)

sql = """INSERT INTO categories(name, description) 
        VALUES('Dodatkowe', 'kupienie czegoś dla siebie');"""
cursor.execute(sql)

sql = """INSERT INTO categories(name, description) 
        VALUES('Nieprzewidziane', 'coś co trudno było przewidzieć');"""
cursor.execute(sql)

close_connection(cnx, cursor)
