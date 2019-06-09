# GroceryHelper

## Purpose
GroceryHelper is a simple text-based CLI program designed to help users keep track of their groceries.

### Features

- Stores user-described groceries and recipes in MongoDB database as standardized documents
- Shows organized display of user's inventory and recipes
- Identifies items that either have or will soon expire

## Usage
To run: `$ python3 GroceryHelper.py`

### Database
Addtionally, a MongoDB instance must be running for the app to function correctly. You must also have a configuration YAML file. By default the program searches for a file named "config.yaml" (based off "config_example.yaml") in the same directory as "GroceryHelper.py". If you wish to use a different configuaration filename, you may specify it as a command line argument. Example:

`$ python3 GroceryHelper.py my_config_file.yaml`

Quickstart for Local Use:

`$ cp config_example.yaml config.yaml`

The default collections are "product" and "recipe".

### Packages

To install packages run:

`$ pip install -r requirements.txt`
