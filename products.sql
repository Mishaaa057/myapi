CREATE TABLE products (
  id INT NOT NULL,
  store_id INT NOT NULL,
  price VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  url VARCHAR(255) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (store_id) REFERENCES stores(id)
);

INSERT INTO products (id, store_id, price, name, url)
VALUES (1, 1, 49.99, 'Samsung Phone', 'https://www.amazon.com/echo-dot'),
       (2, 2, 1229.99, 'TV', 'https://www.walmart.com/samsung-tv'),
       (3, 1, 499.99, 'Laptop', 'https://www.amazon.com/fire-stick'),
       (4, 3, 299.99, 'Apple Watch', 'https://www.target.com/ipad');

SELECT p.id, s.name AS store_name, p.price, p.name, p.url
FROM products p
JOIN stores s ON p.store_id = s.id;