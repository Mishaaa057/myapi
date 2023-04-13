from flask import Flask
import psycopg2


app = Flask(__name__)

def get_data(query):
    # establish connection
    cnx = psycopg2.connect(user='postgres', password='qwerty',
                       host='localhost', database='mydb', port='5432')

    # create cursor
    cursor = cnx.cursor()

    # execute query
    cursor.execute(query)

    # fetch results
    results = cursor.fetchall()

    # close cursor and connection
    cursor.close()
    cnx.close()

    # return results
    return results

def get_all_stores():
    query = "SELECT * FROM stores"
    return get_data(query)

def get_store_info(store_id):
    query = f"SELECT id, name, url FROM stores WHERE id = {store_id}"
    return get_data(query)[0]

def get_all_store_products(store_id):
    query = f"""SELECT p.id, s.name AS store_name, p.price, p.name, p.url
               FROM products p
               JOIN stores s ON p.store_id = s.id
               WHERE s.id = {store_id}"""
    return get_data(query)    

def get_product_info(product_id, store_id):
    query = f"""SELECT p.id, s.name AS store_name, p.price, p.name, p.url
               FROM products p
               JOIN stores s ON p.store_id = s.id
               WHERE p.id = {product_id} AND s.id = {store_id}"""
    return get_data(query)[0]

print(get_all_stores())

# Show all stores
@app.route("/stores", methods=["GET"])
def stores():
    result = []

    for store in get_all_stores():
        result.append({"id": store[0], "name": store[1], "url": store[2]})
    return result

# Show store information by id
@app.route("/stores/<store_id>", methods=["GET"])
def stores_id(store_id):
    store = get_store_info(store_id)
    return {"id": store[0], "name": store[1], "url": store[2]}

# Show products of store
@app.route("/stores/<store_id>/products", methods=["GET"])
def products_of_store(store_id):
    result = []
    products = get_all_store_products(store_id)
    for product in products:
        result.append({"id":product[0],"store":product[1], "name":product[2], "url":product[3]})
    return result

# Show product information
@app.route("/stores/<store_id>/products/<product_id>", methods=["GET"])
def product(store_id, product_id):
    product = get_product_info(product_id, store_id)
    return {"id":product[0],"store":product[1], "name":product[2], "url":product[3]}


