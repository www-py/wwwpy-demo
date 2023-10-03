CREATE TABLE pie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    flavor TEXT NOT NULL,
    size REAL NOT NULL,
    ingredients TEXT
);
GO
INSERT INTO pie (name, flavor, size, ingredients)
VALUES
('Apple Pie', 'Apple', 9.0, 'Apples, Sugar, Flour, Butter, Cinnamon'),
('Cherry Pie', 'Cherry', 8.5, 'Cherries, Sugar, Flour, Butter'),
('Pumpkin Pie', 'Pumpkin', 10.0, 'Pumpkin Puree, Sugar, Eggs, Cream, Cinnamon, Nutmeg');
GO

CREATE TABLE person
(
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT    NOT NULL,
    surname TEXT    NOT NULL,
    age     INTEGER NOT NULL
);
GO
INSERT INTO person (name, surname, age) VALUES
('Harry', 'Potter', 21),
('Hermione', 'Granger', 21),
('Ron', 'Weasley', 21),
('Jon', 'Snow', 25),
('Arya', 'Stark', 18),
('Daenerys', 'Targaryen', 25),
('Frodo', 'Baggins', 50),
('Aragorn', 'Elessar', 87),
('Legolas', 'Greenleaf', 2931),
('Luke', 'Skywalker', 25),
('Leia', 'Organa', 25),
('Han', 'Solo', 30),
('Peter', 'Parker', 18),
('Tony', 'Stark', 40),
('Bruce', 'Wayne', 35),
('Clark', 'Kent', 30),
('Diana', 'Prince', 800),
('Sherlock', 'Holmes', 35),
('John', 'Watson', 40),
('Percy', 'Jackson', 17),
('Annabeth', 'Chase', 17),
('Katniss', 'Everdeen', 17),
('Peeta', 'Mellark', 17),
('Edward', 'Cullen', 104),
('Bella', 'Swan', 18),
('Walter', 'White', 50),
('Jesse', 'Pinkman', 26),
('Tyrion', 'Lannister', 33),
('Joffrey', 'Baratheon', 19),
('Samwell', 'Tarly', 20),
('Gandalf', 'Grey', 2019),
('Bilbo', 'Baggins', 111),
('Thor', 'Odinson', 1500),
('Loki', 'Laufeyson', 1050),
('Steve', 'Rogers', 101),
('Natasha', 'Romanoff', 35),
('Erik', 'Lensherr', 40),
('Charles', 'Xavier', 40),
('Logan', 'Howlett', 137),
('Jean', 'Grey', 28),
('Scott', 'Summers', 28),
('Ororo', 'Munroe', 30),
('Remy', 'LeBeau', 30),
('Kurt', 'Wagner', 25),
('Raven', 'Darkholme', 25),
('Hank', 'McCoy', 30),
('Buffy', 'Summers', 24),
('Spike', 'Pratt', 120),
('Willow', 'Rosenberg', 24),
('Xander', 'Harris', 24),
('Rupert', 'Giles', 50),
('Cordelia', 'Chase', 24),
('Wesley', 'Wyndam-Pryce', 30),
('Fred', 'Burkle', 25),
('Winifred', 'Burkle', 25),
('Lorne', 'Krevlornswath', 100),
('Charles', 'Gunn', 25),
('Lindsey', 'McDonald', 30),
('Lilah', 'Morgan', 30),
('Ned', 'Stark', 40),
('Catelyn', 'Stark', 40),
('Robb', 'Stark', 20),
('Sansa', 'Stark', 18),
('Bran', 'Stark', 15),
('Rickon', 'Stark', 12),
('Theon', 'Greyjoy', 25),
('Yara', 'Greyjoy', 30),
('Eddard', 'Stark', 40),
('Lyanna', 'Stark', 16),
('Rhaegar', 'Targaryen', 25),
('Viserys', 'Targaryen', 23),
('Khal', 'Drogo', 30),
('Jorah', 'Mormont', 50),
('Barristan', 'Selmy', 60),
('Varys', 'Illyrio', 55),
('Petyr', 'Baelish', 35),
('Cersei', 'Lannister', 35),
('Jaime', 'Lannister', 35),
('Tywin', 'Lannister', 60),
('Kevan', 'Lannister', 55),
('Martyn', 'Lannister', 25),
('Tommen', 'Baratheon', 14),
('Myrcella', 'Baratheon', 16),
('Stannis', 'Baratheon', 40),
('Renly', 'Baratheon', 30),
('Robert', 'Baratheon', 36),
('Shireen', 'Baratheon', 15),
('Melisandre', 'Asshai', 400),
('Davos', 'Seaworth', 40),
('Brienne', 'Tarth', 25),
('Tormund', 'Giantsbane', 40),
('Sandor', 'Clegane', 35),
('Gregor', 'Clegane', 38),
('Roose', 'Bolton', 45)
