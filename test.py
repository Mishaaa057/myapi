from requests import get

url = "http://127.0.0.1:5000/stores/1/products/1"
result = get(url)
print(result.content)