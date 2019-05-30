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
Addtionally, a MongoDB instance must be running for the API to function correctly. You must also have a configuration file named "config.json" (based off "config_example.json") in the same directory as "GroceryHelper.py"

Quickstart for Local Use:

`$ cp config_example.json config.json`

The default collections are "product" and "recipe".

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
	- JSON format must be as follows:
	```
		{
			"prodType" : "example name",
			"expDate": "1/1/1970",
			"note": "example note"
		}
	```
- **/add-recipe**
	- Methods: `POST`
	- Used to create new Recipe object
	- JSON format must be as follows:
	```
		{
			"rcpName": "example name",
			"ingredients": {
				"example ingredient name" : 4,
				"example ingredient name" : 2
			},
			"instructions": "example instructions"
		}
	```
- **/delete-product**
	- Methods: `POST`
	- Used to delete one or all Product objects
	- JSON format must be as follows:
	```
		{
			"prodId": "last four characters of Mongo _id"
		}
	```
- **/delete-recipe**
	- Methods: `POST`
	- Used to delete one or all Recipe objects
	- JSON format must be as follows:
	```
		{
			"rcpId": "last four characters of Mongo _id"
		}
	```

### Packages
You must install the flask package and the flask-mongoengine package. This can be done with

`pip install flask`

`pip install flask-mongoengine`

or they can be found here:

http://flask.pocoo.org/

http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/
