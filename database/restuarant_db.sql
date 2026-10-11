-------------------------------------
--Author: ASHLEY NTABISO MONDELA
--Tool: PostgreSQL v18
--Time taken: 2 Months, 6 days
-- Purpose: Restuarant Database
-------------------------------------





CREATE TABLE category (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE CHECK (name IN ('Chinese', 'Italian', 'Mexican', 'Turkish', 'Zimbabwean'))
);
INSERT INTO category (name) VALUES
('Chinese'),
('Italian'),
('Mexican'),
('Turkish'),
('Zimbabwean');
CREATE TABLE ingredient (
    ing_no SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    amount DECIMAL(10,2) NOT NULL CHECK (amount >= 0),
    unit VARCHAR(20) NOT NULL CHECK (unit IN ('kg', 'g', 'L', 'ml', 'pieces', 'cups', 'tbsp', 'tsp'))
);

INSERT INTO ingredient (name, amount, unit) VALUES
-- General
('Salt', 5.00, 'kg'),
('Black Pepper', 2.00, 'kg'),
('Garlic', 5.00, 'kg'),
('Onion', 15.00, 'kg'),
('Olive Oil', 10.00, 'L'),
('Butter', 8.00, 'kg'),
('Sugar', 10.00, 'kg'),
('Flour', 30.00, 'kg'),
('Egg', 200.00, 'pieces'),
('Milk', 15.00, 'L'),
('Lemon', 5.00, 'kg'),
('Tomato', 20.00, 'kg'),
---Chinese
('Rice', 50.00, 'kg'),
('Chicken', 30.00, 'kg'),
('Soy Sauce', 5.00, 'L'),
('Ginger', 2.00, 'kg'),
('Sesame Oil', 3.00, 'L'),
('Spring Onion', 4.00, 'kg'),
('Tofu', 6.00, 'kg'),
('Chili Pepper', 3.00, 'kg'),
('Chili Bean Paste', 2.00, 'kg'),
('Peanuts', 10.00, 'kg'),
('Wonton Wrapper', 5.00, 'kg'),
('Hoisin Sauce', 2.00, 'L'),
('Duck', 15.00, 'kg'),
('Five Spice Powder', 1.00, 'kg'),
('Bamboo Shoots', 3.00, 'kg'),
-- Italian
('Pasta', 25.00, 'kg'),
('Beef', 20.00, 'kg'),
('Bacon', 6.00, 'kg'),
('Heavy Cream', 5.00, 'L'),
('Mozzarella', 8.00, 'kg'),
('Cheese', 10.00, 'kg'),
('Basil', 1.00, 'kg'),
('Oregano', 0.50, 'kg'),
('Arborio Rice', 8.00, 'kg'),
('White Wine', 3.00, 'L'),
('Parmesan', 5.00, 'kg'),
('Mascarpone', 4.00, 'kg'),
('Espresso', 2.00, 'L'),
('Cocoa Powder', 1.00, 'kg'),
('Ladyfinger Biscuits', 3.00, 'kg'),
('Breadcrumbs', 2.00, 'kg'),
-- Mexican
('Avocado', 8.00, 'kg'),
('Corn Tortilla', 10.00, 'pieces'),
('Kidney Beans', 10.00, 'kg'),
('Cumin', 1.50, 'kg'),
('Paprika', 1.50, 'kg'),
('Coriander', 1.00, 'kg'),
('Jalapeno', 2.00, 'kg'),
('Sour Cream', 4.00, 'kg'),
('Pork', 15.00, 'kg'),
('Cinnamon', 0.50, 'kg'),
('Chocolate', 3.00, 'kg'),
('Nachos Chips', 8.00, 'kg'),
-- Turkish
('Lamb', 15.00, 'kg'),
('Eggplant', 5.00, 'kg'),
('Chickpeas', 8.00, 'kg'),
('Tahini', 3.00, 'kg'),
('Red Lentils', 10.00, 'kg'),
('Pistachios', 4.00, 'kg'),
('Phyllo Dough', 5.00, 'kg'),
('Honey', 3.00, 'L'),
('Yogurt', 8.00, 'kg'),
('Thyme', 0.50, 'kg'),
('Sumac', 0.50, 'kg'),
('Rice Pudding Mix', 3.00, 'kg'),
('Pide Dough', 6.00, 'kg'),
-- Zimbabwean
('Mealie Meal', 40.00, 'kg'),
('Beef Intestines', 5.00, 'kg'),
('Dried Fish', 4.00, 'kg'),
('Mopane Worms', 3.00, 'kg'),
('Pumpkin Leaves', 5.00, 'kg'),
('Spinach', 6.00, 'kg'),
('Groundnut Paste', 4.00, 'kg'),
('Cow Trotters', 6.00, 'kg'),
('Sorghum', 8.00, 'kg'),
('Mahewu Powder', 5.00, 'kg'),
('Coconut Milk', 8.00, 'L'),
('Bell Pepper', 10.00, 'kg'),
('Mushroom', 8.00, 'kg');

CREATE TABLE supplier (
    supplier_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE,
    address VARCHAR(200) NOT NULL,
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO supplier (name, phone, address, email) VALUES
('Fresh Farms Ltd', '+90-555-1001', '12 Market Street, Nicosia', 'freshfarms@email.com'),
('Mediterranean Supplies', '+90-555-1002', '45 Harbor Road, Kyrenia', 'medsupplies@email.com'),
('Global Spice Co', '+90-555-1003', '78 Trade Avenue, Famagusta', 'globalspice@email.com'),
('Asian Food Imports', '+90-555-1004', '23 East Boulevard, Nicosia', 'asianfood@email.com'),
('Local Harvest TRNC', '+90-555-1005', '56 Farm Road, Morphou', 'localharvest@email.com'),
('African Cuisine Supplies', '+90-555-1006', '34 South Street, Nicosia', 'africancuisine@email.com');


CREATE TABLE supplier_ingredient (
    supplier_id INT NOT NULL REFERENCES supplier(supplier_id),
    ing_no INT NOT NULL REFERENCES ingredient(ing_no),
    PRIMARY KEY (supplier_id, ing_no)
);

INSERT INTO supplier_ingredient (supplier_id, ing_no) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 13), (1, 14),
(2, 5), (2, 6), (2, 28), (2, 29), (2, 32), (2, 33),
(3, 15), (3, 16), (3, 17), (3, 21), (3, 26), (3, 27),
(4, 18), (4, 19), (4, 20), (4, 22), (4, 23), (4, 24),
(5, 7), (5, 8), (5, 9), (5, 10), (5, 11), (5, 12),
(6, 69), (6, 70), (6, 71), (6, 72), (6, 73), (6, 74);

CREATE TABLE tables (
    table_id SERIAL PRIMARY KEY,
    capacity INT NOT NULL CHECK (capacity > 0),
    location VARCHAR(50) NOT NULL CHECK (location IN ('Indoor', 'Outdoor', 'VIP', 'Terrace')),
    status VARCHAR(20) NOT NULL DEFAULT 'Available' CHECK (status IN ('Available', 'Occupied', 'Reserved'))
);

INSERT INTO tables (capacity, location, status) VALUES
(2, 'Indoor', 'Available'),
(4, 'Indoor', 'Available'),
(4, 'Outdoor', 'Available'),
(6, 'Outdoor', 'Available'),
(2, 'VIP', 'Available'),
(8, 'VIP', 'Available'),
(4, 'Terrace', 'Available'),
(6, 'Terrace', 'Available'),
(2, 'Indoor', 'Available'),
(4, 'Indoor', 'Available');

CREATE TABLE employee (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('Waiter', 'Waitress', 'Chef', 'Manager', 'Cashier')),
    phone VARCHAR(20) NOT NULL UNIQUE,
    address VARCHAR(200) NOT NULL,
    salary DECIMAL(10,2) NOT NULL CHECK (salary > 0),
    hire_date DATE NOT NULL
);
INSERT INTO employee (name, role, phone, address, salary, hire_date) VALUES
('Ahmed Yilmaz', 'Manager', '+90-555-2001', '23 Ataturk Street, Nicosia', 5000.00, '2020-01-15'),
('Maria Santos', 'Chef', '+90-555-2002', '45 Palm Avenue, Kyrenia', 4500.00, '2020-03-20'),
('Vincent Koroma', 'Waiter', '+90-555-2003', '12 Cedar Road, Nicosia', 2500.00, '2021-06-10'),
('Fatima Al-Hassan', 'Waitress', '+90-555-2004', '78 Olive Street, Famagusta', 2500.00, '2021-08-15'),
('Mark Miti', 'Chef', '+90-555-2005', '34 Harbor Road, Kyrenia', 4000.00, '2021-09-01'),
('Ashley Mondela', 'Waiter', '+90-555-2006', '56 University Road, Nicosia', 2500.00, '2022-01-10'),
('Mzwandile Setlhare', 'Waitress', '+90-555-2007', '89 Market Street, Nicosia', 2500.00, '2022-03-15'),
('Munashe Matimbira', 'Chef', '+90-555-2008', '23 South Avenue, Kyrenia', 4000.00, '2022-06-20'),
('Prince Jonas', 'Cashier', '+90-555-2009', '45 East Road, Nicosia', 3000.00, '2022-09-01'),
('Junior Ncube', 'Waitress', '+90-555-2010', '67 West Street, Famagusta', 2500.00, '2023-01-15');

CREATE TABLE customer (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE,
    address VARCHAR(200) NOT NULL,
    email VARCHAR(100) UNIQUE,
    country VARCHAR(100) NOT NULL DEFAULT 'Unknown',
    join_date DATE DEFAULT CURRENT_DATE
);

INSERT INTO customer (name, phone, address, email, country, join_date) VALUES
('John Smith', '+44-755-3001', '15 Baker Street, London', 'john.smith@email.com', 'United Kingdom', '2023-01-10'),
('Aisha Mohammed', '+971-50-3002', '23 Sheikh Zayed Road, Dubai', 'aisha.m@email.com', 'UAE', '2023-02-15'),
('David Cheng', '+86-139-3003', '88 Nanjing Road, Shanghai', 'david.c@email.com', 'China', '2023-03-20'),
('Elena Petrova', '+7-916-3004', '45 Arbat Street, Moscow', 'elena.p@email.com', 'Russia', '2023-04-25'),
('Kwame Asante', '+233-24-3005', '12 Independence Avenue, Accra', 'kwame.a@email.com', 'Ghana', '2023-05-30'),
('Yuki Tanaka', '+81-90-3006', '7 Shibuya Crossing, Tokyo', 'yuki.t@email.com', 'Japan', '2023-06-15'),
('Sofia Garcia', '+34-612-3007', '34 Gran Via, Madrid', 'sofia.g@email.com', 'Spain', '2023-07-20'),
('Mohammed Al-Farsi', '+968-92-3008', '56 Muttrah Corniche, Muscat', 'mohammed.f@email.com', 'Oman', '2023-08-25'),
('Chidi Obi', '+234-80-3009', '23 Victoria Island, Lagos', 'chidi.o@email.com', 'Nigeria', '2023-09-30'),
('Isabella Rossi', '+39-333-3010', '15 Via Veneto, Rome', 'isabella.r@email.com', 'Italy', '2023-10-15'),
('Tariq Hassan', '+20-100-3011', '78 Tahrir Square, Cairo', 'tariq.h@email.com', 'Egypt', '2023-11-20'),
('Priya Sharma', '+91-98-3012', '45 MG Road, Bangalore', 'priya.s@email.com', 'India', '2023-12-25'),
('Lucas Fernandez', '+55-11-3013', '23 Paulista Avenue, Sao Paulo', 'lucas.f@email.com', 'Brazil', '2024-01-10'),
('Amina Diallo', '+221-77-3014', '12 Avenue Cheikh Anta Diop, Dakar', 'amina.d@email.com', 'Senegal', '2024-02-15'),
('Ryan Müller', '+49-151-3015', '67 Unter den Linden, Berlin', 'ryan.m@email.com', 'Germany', '2024-03-20'),
('Tatenda Moyo', '+263-77-3016', '23 Borrowdale Road, Harare', 'tatenda.m@email.com', 'Zimbabwe', '2024-04-05'),
('Chiedza Mpofu', '+263-71-3017', '45 Samora Machel Avenue, Harare', 'chiedza.m@email.com', 'Zimbabwe', '2024-04-10'),
('Farai Mutasa', '+263-73-3018', '67 Julius Nyerere Way, Harare', 'farai.m@email.com', 'Zimbabwe', '2024-04-15'),
('Nyasha Chirwa', '+263-78-3019', '89 Robert Mugabe Road, Bulawayo', 'nyasha.c@email.com', 'Zimbabwe', '2024-04-20'),
('Tendai Ncube', '+263-71-3020', '12 Lobengula Street, Bulawayo', 'tendai.n@email.com', 'Zimbabwe', '2024-05-01'),
('Sipho Dlamini', '+27-82-3021', '34 Sandton Drive, Johannesburg', 'sipho.d@email.com', 'South Africa', '2024-05-05'),
('Thandiwe Nkosi', '+27-73-3022', '56 Long Street, Cape Town', 'thandiwe.n@email.com', 'South Africa', '2024-05-10'),
('Lungelo Zulu', '+27-83-3023', '78 Florida Road, Durban', 'lungelo.z@email.com', 'South Africa', '2024-05-15'),
('Nomvula Dube', '+27-72-3024', '23 Commissioner Street, Johannesburg', 'nomvula.d@email.com', 'South Africa', '2024-05-20'),
('Blessing Mokoena', '+27-84-3025', '45 Church Street, Pretoria', 'blessing.m@email.com', 'South Africa', '2024-05-25'),
('Tinashe Banda', '+263-77-3026', '67 Harare Drive, Mutare', 'tinashe.b@email.com', 'Zimbabwe', '2024-06-01'),
('Rudo Chikwanda', '+263-71-3027', '89 Main Street, Gweru', 'rudo.c@email.com', 'Zimbabwe', '2024-06-05'),
('Simbarashe Mhere', '+263-73-3028', '12 Victoria Falls Road, Victoria Falls', 'simba.m@email.com', 'Zimbabwe', '2024-06-10'),
('Kudzai Mutendi', '+263-78-3029', '34 Masvingo Road, Masvingo', 'kudzai.m@email.com', 'Zimbabwe', '2024-06-15'),
('Thabo Sithole', '+27-83-3030', '56 Nelson Mandela Boulevard, Cape Town', 'thabo.s@email.com', 'South Africa', '2024-06-20');

CREATE TABLE meal (
    meal_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    price DECIMAL(10,2) NOT NULL CHECK (price > 0),
    time INT NOT NULL CHECK (time > 0),
    category_id INT NOT NULL REFERENCES category(category_id)
);

INSERT INTO meal (name, price, time, category_id) VALUES
-- Chinese
('Kung Pao Chicken', 18.50, 20, 1),
('Fried Rice', 12.00, 15, 1),
('Spring Rolls', 8.50, 10, 1),
('Sweet and Sour Pork', 19.00, 25, 1),
('Dim Sum', 14.00, 20, 1),
('Peking Duck', 35.00, 45, 1),
('Mapo Tofu', 14.50, 20, 1),
('Wonton Soup', 10.00, 15, 1),
-- Italian
('Spaghetti Carbonara', 16.00, 20, 2),
('Margherita Pizza', 14.50, 25, 2),
('Lasagna', 17.00, 40, 2),
('Risotto', 15.50, 30, 2),
('Tiramisu', 8.00, 5, 2),
('Bruschetta', 7.50, 10, 2),
('Fettuccine Alfredo', 16.50, 20, 2),
('Panna Cotta', 7.00, 5, 2),
-- Mexican
('Tacos Al Pastor', 13.00, 15, 3),
('Guacamole', 7.50, 10, 3),
('Enchiladas', 15.00, 25, 3),
('Burrito', 14.00, 20, 3),
('Churros', 6.50, 15, 3),
('Quesadilla', 12.00, 15, 3),
('Nachos', 9.00, 10, 3),
('Chiles Rellenos', 16.00, 30, 3),
-- Turkish
('Adana Kebab', 18.00, 25, 4),
('Hummus', 7.00, 10, 4),
('Baklava', 6.00, 5, 4),
('Pide', 12.00, 20, 4),
('Lentil Soup', 8.00, 15, 4),
('Iskender Kebab', 20.00, 30, 4),
('Meze Platter', 15.00, 15, 4),
('Sutlac', 6.50, 5, 4),
-- Zimbabwean (Ndebele)
('Isitshwala lenyama yenkomo', 15.00, 30, 5),
('Isitshwala lezangaphakathi', 12.00, 25, 5),
('Gango', 8.00, 15, 5),
('Isistshwala laMatemba', 11.00, 20, 5),
('Isitshwala laMacimbi', 13.00, 15, 5),
('Isitshwala soLude', 18.00, 35, 5),
('Itshakada', 10.00, 20, 5),
('Isitshwala lombhida', 5.00, 5, 5);

CREATE TABLE meal_ingre (
    meal_id INT NOT NULL REFERENCES meal(meal_id),
    ing_no INT NOT NULL REFERENCES ingredient(ing_no),
    PRIMARY KEY (meal_id, ing_no)
);

INSERT INTO meal_ingre (meal_id, ing_no) VALUES
-- Kung Pao Chicken
(1, 14), (1, 20), (1, 15), (1, 16), (1, 3), (1, 1),
-- Fried Rice
(2, 13), (2, 9), (2, 15), (2, 18), (2, 1),
-- Spring Rolls
(3, 23), (3, 4), (3, 27), (3, 15),
-- Sweet and Sour Pork
(4, 53), (4, 12), (4, 7), (4, 15),
-- Dim Sum
(5, 23), (5, 14), (5, 18), (5, 15),
-- Peking Duck
(6, 25), (6, 26), (6, 24), (6, 15),
-- Mapo Tofu
(7, 19), (7, 21), (7, 20), (7, 3), (7, 15),
-- Wonton Soup
(8, 23), (8, 14), (8, 18), (8, 1),
-- Spaghetti Carbonara
(9, 28), (9, 29), (9, 30), (9, 32), (9, 1),
-- Margherita Pizza
(10, 31), (10, 12), (10, 33), (10, 34),
-- Lasagna
(11, 28), (11, 29), (11, 12), (11, 32), (11, 1),
-- Risotto
(12, 35), (12, 36), (12, 37), (12, 6),
-- Tiramisu
(13, 38), (13, 39), (13, 40), (13, 10), (13, 7),
-- Bruschetta
(14, 12), (14, 33), (14, 5), (14, 1),
-- Fettuccine Alfredo
(15, 28), (15, 30), (15, 37), (15, 6),
-- Panna Cotta
(16, 30), (16, 10), (16, 7),
-- Tacos Al Pastor
(17, 47), (17, 53), (17, 20), (17, 46),
-- Guacamole
(18, 44), (18, 12), (18, 11), (18, 1),
-- Enchiladas
(19, 47), (19, 14), (19, 12), (19, 32),
-- Burrito
(20, 47), (20, 48), (20, 44), (20, 13),
-- Churros
(21, 8), (21, 7), (21, 9), (21, 51),
-- Quesadilla
(22, 47), (22, 32), (22, 14),
-- Nachos
(23, 52), (23, 32), (23, 44), (23, 49),
-- Chiles Rellenos
(24, 20), (24, 32), (24, 12), (24, 9),
-- Adana Kebab
(25, 56), (25, 4), (25, 45), (25, 1),
-- Hummus
(26, 59), (26, 60), (26, 5), (26, 11),
-- Baklava
(27, 63), (27, 64), (27, 61),
-- Pide
(28, 65), (28, 14), (28, 32), (28, 1),
-- Lentil Soup
(29, 61), (29, 4), (29, 3), (29, 1),
-- Iskender Kebab
(30, 56), (30, 12), (30, 6), (30, 66),
-- Meze Platter
(31, 26), (31, 57), (31, 44), (31, 5),
-- Sutlac
(32, 68), (32, 10), (32, 7),
-- Isitshwala lenyama yenkomo
(33, 69), (33, 29), (33, 1),
-- Isitshwala lezangaphakathi
(34, 69), (34, 70), (34, 1),
-- Gango
(35, 71), (35, 4), (35, 1),
-- Isistshwala laMatemba
(36, 69), (36, 72), (36, 1),
-- Isitshwala laMacimbi
(37, 69), (37, 73), (37, 1),
-- Isitshwala soLude
(38, 69), (38, 74), (38, 1),
-- Itshakada
(39, 75), (39, 4), (39, 1),
-- Isitshwala lombhida
(40, 69), (40, 76), (40, 1);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    time TIME NOT NULL DEFAULT CURRENT_TIME,
    tip DECIMAL(10,2) DEFAULT 0.00 CHECK (tip >= 0),
    customer_id INT NOT NULL REFERENCES customer(customer_id),
    employee_id INT NOT NULL REFERENCES employee(employee_id),
    table_id INT NOT NULL REFERENCES tables(table_id)
);

INSERT INTO orders (date, time, tip, customer_id, employee_id, table_id) VALUES
('2024-01-10', '12:30:00', 5.00, 1, 3, 1),
('2024-01-15', '13:00:00', 8.00, 2, 6, 2),
('2024-01-20', '14:00:00', 3.00, 3, 4, 3),
('2024-02-05', '19:00:00', 10.00, 4, 7, 4),
('2024-02-14', '20:00:00', 15.00, 5, 3, 5),
('2024-02-20', '12:00:00', 5.00, 6, 6, 6),
('2024-03-01', '13:30:00', 7.00, 7, 4, 7),
('2024-03-10', '18:00:00', 12.00, 8, 7, 8),
('2024-03-15', '19:30:00', 6.00, 9, 3, 9),
('2024-03-20', '20:00:00', 9.00, 10, 6, 10),
('2024-04-01', '12:00:00', 4.00, 11, 4, 1),
('2024-04-10', '13:00:00', 11.00, 12, 7, 2),
('2024-04-15', '14:30:00', 8.00, 13, 3, 3),
('2024-04-20', '19:00:00', 6.00, 14, 6, 4),
('2024-05-01', '20:00:00', 13.00, 15, 4, 5),
('2024-05-10', '12:30:00', 7.00, 16, 7, 6),
('2024-05-15', '13:00:00', 5.00, 17, 3, 7),
('2024-05-20', '18:00:00', 9.00, 18, 6, 8),
('2024-06-01', '19:00:00', 10.00, 19, 4, 9),
('2024-06-10', '20:30:00', 14.00, 20, 7, 10),
('2024-06-15', '12:00:00', 6.00, 21, 3, 1),
('2024-06-20', '13:30:00', 8.00, 22, 6, 2),
('2024-07-01', '14:00:00', 5.00, 23, 4, 3),
('2024-07-10', '19:00:00', 11.00, 24, 7, 4),
('2024-07-15', '20:00:00', 7.00, 25, 3, 5),
('2024-07-20', '12:30:00', 9.00, 26, 6, 6),
('2024-08-01', '13:00:00', 6.00, 27, 4, 7),
('2024-08-10', '18:30:00', 12.00, 28, 7, 8),
('2024-08-15', '19:00:00', 8.00, 29, 3, 9),
('2024-08-20', '20:00:00', 10.00, 30, 6, 10);

CREATE TABLE order_item (
    order_item_id SERIAL PRIMARY KEY,
    quantity INT NOT NULL CHECK (quantity > 0),
    order_id INT NOT NULL REFERENCES orders(order_id),
    meal_id INT NOT NULL REFERENCES meal(meal_id)
);

INSERT INTO order_item (quantity, order_id, meal_id) VALUES
(2, 1, 1), (1, 1, 3),
(1, 2, 9), (2, 2, 14),
(3, 3, 17), (1, 3, 18),
(1, 4, 25), (2, 4, 26),
(2, 5, 33), (1, 5, 35),
(1, 6, 6), (1, 6, 2),
(2, 7, 19), (1, 7, 21),
(1, 8, 30), (2, 8, 27),
(3, 9, 37), (1, 9, 39),
(1, 10, 11), (1, 10, 13),
(2, 11, 22), (1, 11, 23),
(1, 12, 29), (2, 12, 31),
(1, 13, 4), (1, 13, 5),
(2, 14, 34), (1, 14, 36),
(1, 15, 16), (2, 15, 15),
(1, 16, 38), (1, 16, 40),
(2, 17, 8), (1, 17, 7),
(1, 18, 20), (2, 18, 24),
(1, 19, 28), (1, 19, 32),
(2, 20, 33), (1, 20, 34),
(1, 21, 1), (2, 21, 2),
(1, 22, 10), (1, 22, 12),
(2, 23, 17), (1, 23, 18),
(1, 24, 25), (2, 24, 26),
(1, 25, 37), (1, 25, 38),
(2, 26, 6), (1, 26, 3),
(1, 27, 19), (2, 27, 20),
(1, 28, 30), (1, 28, 29),
(2, 29, 35), (1, 29, 36),
(1, 30, 11), (2, 30, 13);

CREATE TABLE payment (
    payment_id SERIAL PRIMARY KEY,
    payment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    method VARCHAR(50) NOT NULL CHECK (method IN ('Cash', 'Credit Card', 'Debit Card', 'Mobile Payment')),
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    order_id INT NOT NULL UNIQUE REFERENCES orders(order_id)
);

INSERT INTO payment (payment_date, method, amount, order_id) VALUES
('2024-01-10', 'Cash', 45.50, 1),
('2024-01-15', 'Credit Card', 38.00, 2),
('2024-01-20', 'Debit Card', 27.50, 3),
('2024-02-05', 'Mobile Payment', 55.00, 4),
('2024-02-14', 'Cash', 30.00, 5),
('2024-02-20', 'Credit Card', 47.00, 6),
('2024-03-01', 'Debit Card', 29.00, 7),
('2024-03-10', 'Mobile Payment', 62.00, 8),
('2024-03-15', 'Cash', 37.00, 9),
('2024-03-20', 'Credit Card', 44.00, 10),
('2024-04-01', 'Debit Card', 25.00, 11),
('2024-04-10', 'Mobile Payment', 51.00, 12),
('2024-04-15', 'Cash', 36.00, 13),
('2024-04-20', 'Credit Card', 28.00, 14),
('2024-05-01', 'Debit Card', 49.00, 15),
('2024-05-10', 'Mobile Payment', 33.00, 16),
('2024-05-15', 'Cash', 22.00, 17),
('2024-05-20', 'Credit Card', 42.00, 18),
('2024-06-01', 'Debit Card', 32.00, 19),
('2024-06-10', 'Mobile Payment', 27.00, 20),
('2024-06-15', 'Cash', 38.50, 21),
('2024-06-20', 'Credit Card', 46.00, 22),
('2024-07-01', 'Debit Card', 29.50, 23),
('2024-07-10', 'Mobile Payment', 53.00, 24),
('2024-07-15', 'Cash', 31.00, 25),
('2024-07-20', 'Credit Card', 41.00, 26),
('2024-08-01', 'Debit Card', 26.00, 27),
('2024-08-10', 'Mobile Payment', 58.00, 28),
('2024-08-15', 'Cash', 35.00, 29),
('2024-08-20', 'Credit Card', 43.00, 30);

CREATE TABLE reservation (
    reservation_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    time TIME NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending' CHECK (status IN ('Pending', 'Confirmed', 'Cancelled')),
    customer_id INT NOT NULL REFERENCES customer(customer_id),
    table_id INT NOT NULL REFERENCES tables(table_id)
);

INSERT INTO reservation (date, time, status, customer_id, table_id) VALUES
('2024-09-01', '12:00:00', 'Confirmed', 1, 1),
('2024-09-05', '13:00:00', 'Confirmed', 2, 2),
('2024-09-10', '19:00:00', 'Pending', 3, 3),
('2024-09-15', '20:00:00', 'Confirmed', 4, 4),
('2024-09-20', '12:30:00', 'Cancelled', 5, 5),
('2024-10-01', '13:00:00', 'Confirmed', 6, 6),
('2024-10-05', '18:00:00', 'Pending', 7, 7),
('2024-10-10', '19:30:00', 'Confirmed', 8, 8),
('2024-10-15', '20:00:00', 'Confirmed', 9, 9),
('2024-10-20', '12:00:00', 'Cancelled', 10, 10),
('2024-11-01', '13:30:00', 'Confirmed', 11, 1),
('2024-11-05', '14:00:00', 'Pending', 12, 2),
('2024-11-10', '19:00:00', 'Confirmed', 13, 3),
('2024-11-15', '20:30:00', 'Confirmed', 14, 4),
('2024-11-20', '12:00:00', 'Cancelled', 15, 5);

CREATE TABLE rate (
    rate_id SERIAL PRIMARY KEY,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment VARCHAR(500),
    customer_id INT NOT NULL REFERENCES customer(customer_id),
    meal_id INT NOT NULL REFERENCES meal(meal_id)
);

INSERT INTO rate (rating, comment, customer_id, meal_id) VALUES
(5, 'Absolutely delicious! Best Kung Pao Chicken I have ever had.', 1, 1),
(4, 'Great Carbonara, very authentic Italian taste.', 2, 9),
(3, 'Tacos were good but a bit spicy for my taste.', 3, 17),
(5, 'Adana Kebab was perfect, just like in Turkey!', 4, 25),
(4, 'Isitshwala lenyama yenkomo reminded me of home.', 5, 33),
(5, 'Peking Duck was absolutely worth the price.', 6, 6),
(4, 'Margherita Pizza was fresh and delicious.', 7, 10),
(3, 'Enchiladas were okay, nothing special.', 8, 19),
(5, 'Iskender Kebab was outstanding!', 9, 30),
(4, 'Gango was very tasty and authentic.', 10, 35),
(5, 'Spring Rolls were crispy and fresh.', 11, 3),
(4, 'Tiramisu was creamy and delightful.', 12, 13),
(3, 'Burrito was filling but could use more seasoning.', 13, 20),
(5, 'Hummus was smooth and perfectly seasoned.', 14, 26),
(4, 'Itshakada was unique and enjoyable.', 15, 39),
(5, 'Dim Sum was amazing, very authentic.', 16, 5),
(4, 'Lasagna was rich and hearty.', 17, 11),
(5, 'Churros were perfectly crispy and sweet.', 18, 21),
(4, 'Baklava was sweet and nutty, loved it.', 19, 27),
(5, 'Isitshwala laMacimbi was a unique experience!', 20, 37);

SELECT tablename FROM pg_tables WHERE schemaname = 'public';