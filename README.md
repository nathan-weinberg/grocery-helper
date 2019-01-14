# GroceryHelper
#### Author: Nathan Weinberg
##### Written in Python 3.6

## Purpose
GroceryHelper is a simple API designed to help users keep track of their groceries.

### Features

- Stores user-described groceries and recipes in MongoDB database as standardized documents
- Can provide organized inventory of user's products and recipes
- Can identify items that either have or will soon expire

## Usage
This file should be run from the command line. Example:

 `$ python3 GroceryHelper.py`

By default the API will be accessable at `http://127.0.0.1:5000`

### Database
Addtionally, a MongoDB instance must be running for the API to function correctly. By default, it will attempt to connect to a database named "ghdb_test". The default collections are "product" and "recipe".

### Routes

- **/**
	- Methods: `GET`
	- Displays test page to interact with other various endpoints
- **/products**
	- Methods: `GET`
	- Returns JSON of all products
- **/recipes**
	- Methods: `GET`
	- Returns JSON of all recipes
- **/expired**
	- Methods: `GET`
	- Returns JSON of all expired products
- **/expiring**
	- Methods: `GET`
	- Returns JSON of all products that will expire within three days
- **/add-product**
	- Methods: `POST`
	- Used to create new Product object
- **/add-recipe**
	- Methods: `POST`
	- Used to create new Recipe object
- **/delete-product**
	- Methods: `POST`
	- Used to delete one or all Product objects
- **/delete-recipe**
	- Methods: `POST`
	- Used to delete one or all Recipe objects

### Packages
You must install the flask package and the flask-mongoengine package. This can be done with

`pip install flask`

`pip install flask-mongoengine`

or they can be found here:

http://flask.pocoo.org/

http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/
