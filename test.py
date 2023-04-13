import psycopg2

def get_product_info(product_id, cnx):
    # create cursor
    cursor = cnx.cursor()
    
    # execute query
    query = f"""SELECT p.id, s.name AS store_name, p.price, p.name, p.url
               FROM products p
               JOIN stores s ON p.store_id = s.id
               WHERE p.id = {product_id}"""
    cursor.execute(query)
    
    # fetch result
    result = cursor.fetchone()

    return result

def get_store_info(store_id, cnx):
    # execute query
    query = f"SELECT id, name, url FROM stores WHERE id = {store_id}"
    cursor.execute(query)

    # fetch results
    result = cursor.fetchone()

    return result

# establish connection
cnx = psycopg2.connect(user='postgres', password='qwerty',
                       host='localhost', database='mydb', port='5432')

# create cursor
cursor = cnx.cursor()

# execute query
query = """SELECT p.id, s.name AS store_name, p.price, p.name, p.url
           FROM products p
           JOIN stores s ON p.store_id = s.id"""
cursor.execute(query)

# fetch results
results = cursor.fetchall()

# process results
for result in results:

    print(result)
print(type(result))

print(get_product_info(2, cnx))
print(get_store_info(1, cnx))

# close cursor and connection
cursor.close()
cnx.close()