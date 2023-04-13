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
    query = f"""SELECT p.id, s.id AS store_id, s.name AS store_name, p.price, p.name, p.url
               FROM products p
               JOIN stores s ON p.store_id = s.id
               WHERE s.id = {store_id}"""
    return get_data(query)    

def get_product_info(product_id, store_id):
    query = f"""
        SELECT p.id, s.id AS store_id, p.price, p.name, p.url, s.name AS store_name
        FROM products p
        JOIN stores s ON p.store_id = s.id
        WHERE s.id = {store_id} AND p.id = {product_id};
    """
    return get_data(query)[0]

print(get_all_stores())

# Show all stores
@app.route("/stores", methods=["GET"])
def stores():
    result = []

    for store in get_all_stores():
        data = {"id": store[0], "name": store[1], "url": store[2]}
        result.append(data)
    return {"data":result, "error":None}

# Show store information by id
@app.route("/stores/<store_id>", methods=["GET"])
def stores_id(store_id):
    try:
        store = get_store_info(store_id)
        data = {"id": store[0], "name": store[1], "url": store[2]}
        return {"data":data, "error":None}
    except:
        return {"data":None, "error":"Store with this id not found"}

# Show products of store
@app.route("/stores/<store_id>/products", methods=["GET"])
def products_of_store(store_id):
    try:
        result = []
        products = get_all_store_products(store_id)
        for product in products:
            result.append({"data":{"id":product[0], "store id":product[1],"price":product[2], "name":product[4], "url":product[5]}, "error":None})
        if result == []:
            return {"data":None, "error":"Store with this id not found"}
        return result
    except:
        return {"data":None, "error":"Store with this id not found"}

# Show product information
@app.route("/stores/<store_id>/products/<product_id>", methods=["GET"])
def product(store_id, product_id):
    try:
        product = get_product_info(product_id, store_id)
        # id store_id price store name url
        return {"data":{"id":product[0], "store id":product[1],"price":product[2], "name":product[4], "url":product[5]}, "error":None}
    except:
        return {"data":None, "error":"Wrong id providen"}
    
@app.errorhandler(404)
def page_not_found(err):
    return "Error 404. Page not found, check your url and try again."


