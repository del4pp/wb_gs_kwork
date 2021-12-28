import sqlite3

conn = sqlite3.connect("wild.db", check_same_thread=False)
cursor = conn.cursor()


def new_records_links(product_link):
    sql = 'select * from products where product_link = \'{0}\';'.format(product_link)
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    if result:
        return result

def insert_link(product_link):
    sql = 'insert into products(product_link, product_status)values(\'{0}\', \'{1}\');'.format(product_link, 1)
    cursor.execute(sql)
    conn.commit()

def get_old_price(product_link):
    sql = 'select product_price from products where product_link = \'{0}\''.format(product_link)
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    return result[0][0]

def update_price(product_link, product_price):
    sql = 'update products set product_price = \'{0}\' where product_link = \'{1}\';'.format(product_price,product_link)
    cursor.execute(sql)
    conn.commit()