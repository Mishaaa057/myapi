from flask import Flask, request
import psycopg2
from colorama import Fore


app = Flask(__name__)

def execute_query(query):
    # establish connection
    cnx = psycopg2.connect(user='postgres', password='qwerty',
                       host='localhost', database='mydb', port='5432')

    # create cursor
    cursor = cnx.cursor()

    # execute query
    cursor.execute(query)

    # I Know that it's wrong, but i dont care
    # I think i will regred it someday...
    # fetchall is needed for GET method and commit for POST
    try:
        results = cursor.fetchall()
    except:
        results = []
        cnx.commit()

    cursor.close()
    cnx.close()

    return results


def get_all_stores():
    query = "SELECT * FROM stores"
    return execute_query(query)


def get_store_info(store_id):
    query = f"SELECT id, name, url FROM stores WHERE id = {store_id}"
    return execute_query(query)[0]


def get_all_store_products(store_id):
    query = f"""SELECT p.id, s.id AS store_id, s.name AS store_name, p.price, p.name, p.url
               FROM products p
               JOIN stores s ON p.store_id = s.id
               WHERE s.id = {store_id}"""
    return execute_query(query)    


def get_product_info(product_id, store_id):
    query = f"""
        SELECT p.id, s.id AS store_id, p.price, p.name, p.url, s.name AS store_name
        FROM products p
        JOIN stores s ON p.store_id = s.id
        WHERE s.id = {store_id} AND p.id = {product_id};
    """
    return execute_query(query)[0]


def add_store_to_db(store_id, store_name, store_url):
    query = f"""
        INSERT INTO stores(id, name, url)
        VALUES ({store_id}, '{store_name}', '{store_url}')
    """
    return execute_query(query)


def is_store_exists(store_id):
    query = f"""
        SELECT * FROM stores WHERE id = {store_id}
    """
    return (execute_query(query) != [])


def update_store(store_id, name, url):
    # Update existing store
    query = f"""
        UPDATE stores
        SET name = '{name}', url = '{url}'
        WHERE id = {store_id}
    """
    return execute_query(query)


def new_store_id():
    # Generate new store id

    # Get list of id's
    query = f"""
        SELECT id FROM stores
    """
    # List of tuples with one integer [(1),(2)...]
    ids = execute_query(query)

    # Get clear list of id's
    for i, element in enumerate(ids):
        ids[i] = element[0]

    try:
        id = 0
        while True:
            if id not in ids:
                return id
            id += 1
    except Exception as err:
        info(f"Problem occured during searching for new id, Error: {err}", 'r')
    return 0


# Show all stores
@app.route("/stores", methods=["GET", "POST"])
def stores():
    result = []

    if request.method == "GET":
        
        for store in get_all_stores():
            data = {"id": store[0], "name": store[1], "url": store[2]}
            result.append(data)
        return {"data":result, "error":None}
    
    # Create new store
    elif request.method == "POST":
        info("Request to create new store")

        data = parse_data() # parse data from posted body
        
        if data['name'] and data['url']:
            name = data["name"]
            url = data["url"]
        else:
            info("Some data is missing", 'r')
            return "Some data is missing"

        # New id should be created
        id = new_store_id()

        store_data = {"id":id, "name":name, "url":url}

        # Check if store with such id already exists
        if is_store_exists(id):
            info(f"Store with id {id} already exists", "r")
            return f"Store with id {id} already exists"

        info(f"New store data: {store_data}")

        try:
            add_store_to_db(id, name, url)
            info("New Store was created")
        except Exception as err:
            info(f"Problem occured - {err}", 'r')

        result = store_data
        return {"data":result, "error":None}



# Show store information by id
@app.route("/stores/<store_id>", methods=["GET", "PUT"])
def stores_id(store_id):
    data = None
    error = None

    if request.method == "GET":
        try:
            store = get_store_info(store_id)
            data = {"id": store[0], "name": store[1], "url": store[2]}
            info(f"Store with id: {store_id} was requested")
            
        except:
            error = f"Store with id - {store_id} not found"
            info(error, "r")
    
    # Update existed store
    elif request.method == "PUT":
        info(f"Update requested for store with id - {store_id}")

        # Check if store exists
        if not is_store_exists(store_id):
            error = f"Store with id {store_id} doesn't exists"
            return {"data": data, "error": error}

        # Get data
        data = parse_data()
        info(f"Parsed data: {data}")

        # Check if everything included
        if data["name"] and data["url"]:
            # Update store
            update_store(store_id, data["name"], data["url"])
            info(f"Store with id {store_id} updated")

        else:
            error = "Missing data"
            info(error, 'r')

    
    return {"data": data, "error": error}


# Get and check converted data from body
def parse_data():
    # Get data from body
    data = None
    
    try:
        data = request.get_data().decode()
    except:
        info("Problem occured during decoding the data", 'r')
        return "Problem occured during decoding the data"

    # Get dictionary data type from raw body
    try:
        data = eval(data)
    except:
        info("Invalid data provided", 'r')
        return "Invalid data provided"
    
    return data


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


# Custom print function for debugging
def info(msg, color='g'):
    if color == "g":
        print(f"{Fore.GREEN}[INFO]{Fore.RESET} - {msg}")
    elif color == "r":
        print(f"{Fore.RED}[ERROR]{Fore.RESET} - {msg}")


if __name__=="__main__":
    app.run(debug=True)
