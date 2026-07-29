# Create sample data to test

## CREATE DATABASE

```sql
CREATE DATABASE ecommerce_sample;
```

## CREATE TABLES

```sql
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    city VARCHAR(50),
    signup_date DATE
);
```

```sql
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price NUMERIC(10,2),
    stock INT
);
```

```sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(customer_id),
    order_date DATE,
    status VARCHAR(20)
);
```

```sql
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT NOT NULL REFERENCES orders(order_id),
    product_id INT NOT NULL REFERENCES products(product_id),
    quantity INT NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL
);
```

```sql
CREATE TABLE payments (
    payment_id INT PRIMARY KEY,
    order_id INT UNIQUE REFERENCES orders(order_id),
    payment_method VARCHAR(30),
    amount NUMERIC(10,2),
    payment_status VARCHAR(20)
);
```

## Insert Data

#### INSERT CUSTOMERS

```sql
INSERT INTO customers (customer_id, name, email, city, signup_date) VALUES
(1, 'Alice Johnson', 'alice@email.com', 'Mumbai', '2024-01-15'),
(2, 'Bob Smith', 'bob@email.com', 'Delhi', '2024-02-10'),
(3, 'Charlie Brown', 'charlie@email.com', 'Bangalore', '2024-02-18'),
(4, 'Diana Roy', 'diana@email.com', 'Pune', '2024-03-05'),
(5, 'Ethan Lee', 'ethan@email.com', 'Mumbai', '2024-04-12');
```

#### INSERT PRODUCTS

```sql
INSERT INTO products (product_id, product_name, category, price, stock) VALUES
(101, 'Laptop', 'Electronics', 75000.00, 10),
(102, 'Mouse', 'Electronics', 1200.00, 100),
(103, 'Keyboard', 'Electronics', 2500.00, 75),
(104, 'Office Chair', 'Furniture', 8500.00, 20),
(105, 'Water Bottle', 'Accessories', 500.00, 200);
```

#### INSERT ORDERS

```sql
INSERT INTO orders (order_id, customer_id, order_date, status) VALUES
(1001, 1, '2024-05-01', 'Delivered'),
(1002, 2, '2024-05-03', 'Delivered'),
(1003, 1, '2024-05-10', 'Pending'),
(1004, 3, '2024-05-12', 'Cancelled'),
(1005, 4, '2024-05-18', 'Delivered'),
(1006, 5, '2024-05-20', 'Delivered'),
(1007, 2, '2024-05-22', 'Pending');
```

#### INSERT ORDER ITEMS

```sql
INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price) VALUES
(1, 1001, 101, 1, 75000.00),
(2, 1001, 102, 2, 1200.00),
(3, 1002, 104, 1, 8500.00),
(4, 1003, 103, 2, 2500.00),
(5, 1004, 105, 5, 500.00),
(6, 1005, 104, 2, 8500.00),
(7, 1006, 101, 1, 75000.00),
(8, 1006, 105, 3, 500.00),
(9, 1007, 102, 4, 1200.00);
```

#### INSERT PAYMENTS

```sql
INSERT INTO payments (payment_id, order_id, payment_method, amount, payment_status) VALUES
(5001, 1001, 'Credit Card', 77400.00, 'Paid'),
(5002, 1002, 'UPI', 8500.00, 'Paid'),
(5003, 1003, 'UPI', 5000.00, 'Pending'),
(5004, 1005, 'Debit Card', 17000.00, 'Paid'),
(5005, 1006, 'Credit Card', 76500.00, 'Paid');
```