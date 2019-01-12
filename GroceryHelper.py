'''
GroceryHelper
Copyright (C) 2019 Nathan Weinberg

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

# GroceryHelper
# Nathan Weinberg
# Coded in Python 3.6

import sys
import datetime
from mongoengine import *

# colors text in Windows command prompt
from colorama import init, Fore, Back, Style
init()

# Class/Function Definitions

class Recipe(Document):
	name = StringField(required=True, unique=True, max_length=50)   # stored in lowercase
	ingredients = DictField(required=True)							# stored as {prodType:qty}
	instructions = StringField(required=True)

	def canMake(self):
		for key in self.ingredients:
			if Product.objects(prodType=key).count() < self.ingredients[key]:
				return False
		return True

	def clearIngredients(self):
		for key in self.ingredients:

			# if only one ingredient of this type used, simply delete
			if self.ingredients[key] == 1:
				Product.objects(prodType=key).delete()
			
			# otherwise get and delete number used
			else:
				for i in range(self.ingredients[key]):
					Product.objects(prodType=key).first().delete()

class Product(Document):
	prodType = StringField(required=True, max_length=50)	# stored as lowercase
	expDate = DateTimeField(required=True)
	note = StringField(max_length=50)

	def isExpired(self):
		if self.expDate < currentDate:
			return True	

	def willExpireSoon(self):
		targetDate = self.expDate - datetime.timedelta(days=3)
		if targetDate < currentDate:
			return True

def checkExpired():
	''' scans through all products and determines what is expired
		offers user choice to delete expired items from inventory
	'''

	# scans through all products
	for product in Product.objects:

		# if product is expired, alert user and prompt if they wish to delete it from inventory
		if product.isExpired():

			while True:
				choice = str(input(product.prodType.capitalize() + ' with ID ' + str(product.id)[-4:] + ' has expired. Do you wish to delete it from your inventory? Y/N ')).lower()
				if choice == 'y':
					product.delete()
					break
				elif choice == 'n':
					break
				else:
					print('\nInvalid choice. Please try again.')

def displayInventory():
	''' Displays all items currently in inventory, as well as total size
		If item is expired item will print in red
	'''

	for product in Product.objects.order_by("prodType", "expDate"):

		prodId = "ID: " + str(product.id)[-4:]
		prodType = str(product.prodType).capitalize()
		expDate = "Expires: " + str(product.expDate)[:-9]
		prodNote = str(product.note)

		printProduct = "{} {} {} {}".format(prodId.ljust(10), prodType.ljust(20), expDate.ljust(20), prodNote.ljust(20))

		# highlight red if item is expired
		if product.isExpired():
			print(Fore.RED + str(printProduct))
			print(Style.RESET_ALL, end='')
		# highlight yellow if item will expire within three days
		elif product.willExpireSoon():
			print(Fore.YELLOW + str(printProduct))
			print(Style.RESET_ALL, end='')
		# print normally otherwise
		else:
			print(printProduct)

	print("\nTotal number of items: " + str(Product.objects.count()))

def addProduct():
	''' takes in a product type, expiration date, any notes
		generates a new Product object
	'''

	while True:
		try:
			# get product type
			prodType = str(input("Please input product type: ")).lower()

			# get expDate month
			while True:
				expMonth = str(input('Product experation month? (MM) Type "0" if none: '))
				if expMonth == '0':
					print('There should probably be a month. Check again.')
				else:
					break

			# get expDate day
			expDay = str(input('Product experation day? (DD) Type "0" if none: '))
			if expDay == '0':
				expDay = '01'

			# get expDate year
			expYear = str(input('Product experation year? (YYYY)? Type "0" if none: '))
			if expYear == '0':
				expYear = str(currentDate.year)

			# Consolidates expDateString and creates expDateClass (datetime object)
			expDateString = ' '.join([expMonth, expDay, expYear])
			expDateClass = datetime.datetime.strptime(expDateString, '%m %d %Y')

			# get product note
			note = str(input('Please input any note you have about this product. Type "0" if none: '))
			if note == "0":
				note = None

			break

		# Loops if user input data incorrectly, causing strptime to throw a ValueError
		except ValueError:
			print('\nPlease enter all fields in the correct format.\n')

	# Creates new Product object and saves it to database
	if note == None:
		newProduct = Product(
			prodType=prodType,
			expDate=expDateClass,
		)
	else:
		newProduct = Product(
			prodType=prodType,
			expDate=expDateClass,
			note=note
		)
	newProduct.save()

def deleteProduct():
	''' deletes one or all items from inventory
	'''

	# immediately returns if no products in db
	if Product.objects.count() == 0:
		print("No items in database.")
		return

	# select product and ensure it is in inventory
	prodId = str(input('Please input the ID of the product you wish to remove, or input "All" to empty inventory: ')).lower()

	if prodId == "all":
		while True:
			deleteConfirmAll = str(input("Are you sure you wish to delete all products from your inventory? Y/N ")).lower()
			if deleteConfirmAll == 'y':
				Product.objects.delete()
				break
			elif deleteConfirmAll == 'n':
				break
			else:
				print('\nInvalid choice. Please try again.')

	else:

		# finds and deletes product after confirmation
		for product in Product.objects():
			targ = str(product.id)[-4:]
			if targ == prodId:
				while True:
					deleteConfirm = str(input("Are you sure you wish to delete " + product.prodType + " with ID " + targ + " from your inventory? Y/N ")).lower()
					if deleteConfirm == 'y':
						product.delete()
						return
					elif deleteConfirm == 'n':
						return
					else:
						print('\nInvalid choice. Please try again.')
		print("Invalid ID. Check inventory and make sure ID is correct.")

def displayRecipes():
	''' displays all recipes in database
	'''

	for recipe in Recipe.objects.order_by("name"):

		rcpName = str(recipe.name).capitalize()
		ingredients = "Ingredients: " + str(recipe.ingredients)
		instructions = "Instructions: " + str(recipe.instructions)
		rcpId = "ID: " + str(recipe.id)[-4:]

		printRecipe = "{}\n{}\n{}\n{}\n".format(rcpName, ingredients, instructions, rcpId)
		print(printRecipe)

	print("Total number of recipes: " + str(Recipe.objects.count()))

def addRecipe():
	''' adds recipe to database
	'''

	while True:
		try:
			# get recipe name
			rcpName = str(input("Please input recipe name: ")).lower()

			# get ingredients
			ingredients = {}
			while True:
				newType = str(input('Please input next ingredient type. If done, type "0": ')).lower()
				if newType in ingredients:
					print("Product already in recipe.")
				elif newType == "0":
					if len(ingredients) == 0:
						print("Recipes must have at least one ingredient.")
					else:
						break
				else:
					newQty = int(input('Please input the quantity needed: '))
					ingredients.update({newType:newQty})

			# get instructions
			instructions = str(input('Please input any note you have about this recipe: '))

			break

		# Loops if user input data incorrectly, causing strptime to throw a ValueError
		except ValueError:
			print('\nPlease enter all fields in the correct format.\n')

	# Creates new Recipe object
	newRecipe = Recipe(
		name=rcpName,
		ingredients=ingredients,
		instructions=instructions
	)
	newRecipe.save()
				
def deleteRecipe():
	''' deletes one or all recipes from database
	'''

	# immediately returns if no recipes in db
	if Recipe.objects.count() == 0:
		print("No recipes in database.")
		return

	# select recipe and ensure it is in inventory
	rcpId = str(input('Please input the ID of the recipe you wish to remove, or input "All" to empty inventory: ')).lower()

	if rcpId == "all":
		while True:
			deleteConfirmAll = str(input("Are you sure you wish to delete all recipes from your inventory? Y/N ")).lower()
			if deleteConfirmAll == 'y':
				Recipe.objects.delete()
				break
			elif deleteConfirmAll == 'n':
				break
			else:
				print('\nInvalid choice. Please try again.')

	else:

		# finds and deletes recipe after confirmation
		for recipe in Recipe.objects():
			targ = str(recipe.id)[-4:]
			if targ == rcpId:
				while True:
					deleteConfirm = str(input("Are you sure you wish to delete " + recipe.name.capitalize() + " with ID " + targ + " from your inventory? Y/N ")).lower()
					if deleteConfirm == 'y':
						recipe.delete()
						return
					elif deleteConfirm == 'n':
						return
					else:
						print('\nInvalid choice. Please try again.')
		print("Invalid ID. Check inventory and make sure ID is correct.")

def makeRecipe():
	''' displays specified recipe for preparation
	    deletes products used if request
	'''

	# immediately returns if no recipes in db
	if Recipe.objects.count() == 0:
		print("No recipes in database.")
		return

	# get target name
	targName = str(input("Please input the name of the recipe you would like to make: ")).lower()

	# retrieve recipe from database
	try:
		recipe = Recipe.objects.get(name=targName)
	except DoesNotExist:
		print("No recipe with that name found in database. Check inventory and make sure name is correct.")
		return

	# check if needed ingredients type/qty in products collection
	flag = True
	if not recipe.canMake():
		while True:
			makeConfirm = str(input("You do not have the ingredients in your inventory for this recipe; view anyway? Y/N ")).lower()
			if makeConfirm == 'y':
				flag = False
				break
			elif makeConfirm == 'n':
				return
			else:
				print('\nInvalid choice. Please try again.')

	# pretty print recipe
	rcpName = str(recipe.name).capitalize()
	ingredients = "Ingredients: " + str(recipe.ingredients)
	instructions = "Instructions: " + str(recipe.instructions)
	printRecipe = "\n{}\n{}\n{}".format(rcpName, ingredients, instructions)
	print(printRecipe)

	# only give delete option if ingredients were indicated as available
	if flag:
		while True:
			clearConfirm = str(input("\nWould you like to delete the ingredients used in this recipe from your inventory? Y/N ")).lower()
			if clearConfirm == 'y':
				recipe.clearIngredients()
				break
			elif clearConfirm == 'n':
				break
			else:
				print('\nInvalid choice. Please try again.')

def displayDev(code):
	''' debug function
	'''
	print()
	if code == 11:
		for product in Product.objects:
			print("product.id: " + str(product.id))
			print("product.prodType: " + str(product.prodType))
			print("product.expDate: " + str(product.expDate))
			print("product.note: " + str(product.note)) 
			print()
	if code == 12:
		for recipe in Recipe.objects:
			print("recipe.id: " + str(recipe.id))
			print("recipe.name: " + str(recipe.name))
			print("recipe.ingredients: " + str(recipe.ingredients))
			print("recipe.instructions: " + str(recipe.instructions)) 
			print()

# Main function
def main(debug):

	try:
		# opens db connection
		if debug:
			connect("ghdb_test", host='localhost', port=27017)
		else:
			connect("ghdb", host='localhost', port=27017)
	except Exception as e:
		print("Database Connection Error: ", e)
		sys.exit()

	# license boilerplate
	print("GroceryHelper Copyright (C) 2019 Nathan Weinberg\nThis program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.\nThis is free software, and you are welcome to redistribute it\nunder certain conditions; type `show c' for details.\n")

	# checks if any products have expired 
	checkExpired()

	while True:

		# updates current date
		currentDate = datetime.datetime.today()

		# display        
		print("\n-------------------------------------------\n               GroceryHelper\nCurrent Date is: " + str(currentDate) + "\n-------------------------------------------\n")
		print("(1) View all products")
		print("(2) Add product")
		print("(3) Delete product")
		print()
		print("(4) View all recipes")
		print("(5) Add recipe")
		print("(6) Delete recipe")
		print("(7) Make recipe")
		print()
		print("(0) Exit Program")

		# scan for user choice
		choice = input("\nMake a selection: ")

		# ensure choice is type int
		try:
			choice = int(choice)
		except ValueError:
			print("\nPlease input a number.")
		else:

			# CLI Formatting
			print()

			# Display inventory
			if choice == 1:
				displayInventory()

			# Input new product
			elif choice == 2:
				addProduct()  

			# Delete product
			elif choice == 3:
				deleteProduct()

			# Display recipes
			elif choice == 4:
				displayRecipes()
				
			# Input new recipe
			elif choice == 5:
				addRecipe()  

			# Delete recipe
			elif choice == 6:
				deleteRecipe()

			# Make recipe
			elif choice == 7:
				makeRecipe()

			# Exit
			elif choice == 0:
				break

			# Dev Display
			elif choice == 11:
				displayDev(11)
			elif choice == 11:
				displayDev(12)

			# Invalid choice
			else:
				print('Invalid choice. Please try again.')

	# Exits program
	print("Goodbye!")

if __name__ == "__main__":
	currentDate = datetime.datetime.today()

	# Debug mode option
	if len(sys.argv) > 1 and sys.argv[1] == 'debug':
		debug = True
	else:
		debug = False

	main(debug)
