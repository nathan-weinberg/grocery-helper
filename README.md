# GroceryHelper

## Purpose
GroceryHelper is a simple application designed to help users keep track of their groceries.

### Features

- Stores user-described groceries and recipes in MongoDB database as standardized documents
- Can provide organized inventory of user's products and recipes
- Can identify items that either have or will soon expire

## Usage
### Backend
To run the backend API for this project:

`$ python3 api.py`

By default the API will be accessable at `http://127.0.0.1:5000`

### Database
A MongoDB instance must be running for the application to function correctly. You must also have a configuration file named "config.json" (based off "config.json.example") in the same directory as the file attemping to use it (either "api.py" or "cli.py").

Quickstart for Local Use:

`$ cp config.json.example config.json`

The default collections are "product" and "recipe".

### CLI
Additionally, a CLI is included. Note that the CLI connects to the database directly using `config.json` and does not require the API to be running (although it does require an active Mongo instance). To run the CLI:

`$ python3 cli.py`

### Frontend
GroceryHelper uses an Angular frontend that is currently under construction. At present it is recommended to use the CLI to interface with the application.

### API Routes

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
To install packages run:

`$ pip install -r requirements.txt`
