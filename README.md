# GroceryHelper
#### Author: Nathan Weinberg
##### Written in Python 3.6

## Purpose
GroceryHelper is a simple text-based CLI program designed to help users keep track of their groceries.

### Features

- Stores user-described groceries and recipes in MongoDB database as standardized documents
- Shows organized display of user's inventory and recipes
- Identifies items that either have or will soon expire

## Usage
This file should be run from the command line. Example:

 `$ python3 GroceryHelper.py`

You can run in debug mode by adding an additonal argument `debug`

### Database
Addtionally, a MongoDB instance must be running for the app to function correctly. By default, it will attempt to connect to a database named "ghdb". If run in debug mode, it will attempt to connect to a database named "ghdb_test". The default collections are "product" and "recipe".

### Packages
You must install the Colorama package and the mongoengine package. This can be done with

`pip install colorama`

`pip install mongoengine`

or they can be found here:

https://pypi.python.org/pypi/colorama

http://mongoengine.org/
