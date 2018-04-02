-- V0.01 of backend database definitions
-- Created on postgres v10

--create schema food;

DROP TABLE IF EXISTS food.recipes;
CREATE TABLE food.recipes(
	recipe_id INTEGER PRIMARY KEY,
	recipe_name TEXT NOT NULL,
	recipe_author TEXT,
	ingredient_list TEXT ARRAY,
	recipe_type TEXT,
	recipe_method_list TEXT ARRAY,
	tags TEXT ARRAY,
);

DROP TABLE IF EXISTS food.ingredients;
CREATE TABLE food.ingredients(
	ing_id INTEGER PRIMARY KEY,
	ing_name TEXT NOT NULL,
	ing_type TEXT,
	ing_unit TEXT NOT NULL,
	ing_price NUMERIC(10, 2) DEFAULT 0 
);


-- Dummy test data
Insert into food.recipes 
	VALUES (
		1,
		'Thai Porridge',
		NULL,
		'{rice, water, mince}'
		'lunch',
		NULL,
		NULL
		);