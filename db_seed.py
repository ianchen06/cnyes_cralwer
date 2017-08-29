"""
   db_seed.py
   ~~~~~~~~~~
   Create MySQL databse table and schema from Model

"""
import peewee

import crawler

db = peewee.MySQLDatabase('news',
        user='admin')

db.create_table(crawler.Cnyes)
