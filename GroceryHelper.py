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

import json
import datetime
from flask import *
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = json.load(open("config.json", "r"))
db = MongoEngine(app)

class Recipe(db.Document):
	name = db.StringField(required=True, unique=True, max_length=50)
	ingredients = db.DictField(required=True)	# stored as {prodType:qty}
	instructions = db.StringField(required=True)

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

class Product(db.Document):
	prodType = db.StringField(required=True, max_length=50)	# stored as lowercase
	expDate = db.DateTimeField(required=True)
	note = db.StringField(max_length=50)

	def isExpired(self):
		currentDate = datetime.datetime.today()
		if self.expDate < currentDate:
			return True	
		else:
			return False

	def willExpireSoon(self):
		currentDate = datetime.datetime.today()
		targetDate = self.expDate - datetime.timedelta(days=3)
		if targetDate < currentDate < self.expDate:
			return True
		else:
			return False

@app.route('/', methods=['GET'])
def index():
	currentDate = datetime.datetime.today()
	return render_template("test.html", currentDate=currentDate)

@app.route('/products', methods=['GET'])
def getProducts():
	''' returns JSON of all documents in product collection
	'''

	data = Product.objects.order_by("prodType", "expDate")
	return jsonify(data)

@app.route('/recipes', methods=['GET'])
def getRecipes():
	''' returns JSON of all documents in recipes collection
	'''

	data = Recipe.objects.order_by("name")
	return jsonify(data)

@app.route('/expired', methods=['GET'])
def getExpired():
	''' returns JSON of all expired products
	'''

	expired = []
	# scans through all products
	for product in Product.objects:
		# if product is expired, add to JSON
		if product.isExpired():
			expired += [product]
	return jsonify(expired)

@app.route('/expiring', methods=['GET'])
def getExpiring():
	''' returns JSON of soon-to-expire products
	'''

	expiring = []
	# scans through all products
	for product in Product.objects:
		# if product is expiring, add to JSON
		if product.willExpireSoon():
			expiring += [product]
	return jsonify(expiring)

@app.route('/add-product', methods=['POST'])
def addProduct():
	''' takes in a product type, expiration date, any notes
		generates a new Product object
	'''

	prodType = request.form.get("prodType").lower()
	expDate = request.form.get("expDate")
	note = request.form.get("note")

	# Creates new Product object and saves it to database
	if note == None:
		newProduct = Product(
			prodType=prodType,
			expDate=expDate,
		)
	else:
		newProduct = Product(
			prodType=prodType,
			expDate=expDate,
			note=note
		)
	newProduct.save()

	return jsonify(success=True)

@app.route('/add-recipe', methods=['POST'])
def addRecipe():
	''' adds recipe to database
	'''

	rcpName = request.form.get("prodType")

	# must manually assemble ingredient form data into dict
	ingredientData = request.form.to_dict()
	print(ingredientData)
	ingredients = {}
	for key in ingredientData:
		if key[:-1] == "item":
			ingredients[ingredientData[key]] = int(ingredientData[key+"qty"])

	instructions = request.form.get("instructions")

	# Creates new Recipe object
	newRecipe = Recipe(
		name=rcpName,
		ingredients=ingredients,
		instructions=instructions
	)
	newRecipe.save()

	return jsonify(success=True)

@app.route('/delete-product', methods=['POST'])
def deleteProduct():
	''' deletes one or all items from inventory
	'''

	# immediately returns if no products in db
	if Product.objects.count() == 0:
		return jsonify(success=False, message="No products in database.")

	# select product and ensure it is in inventory
	prodId = request.form.get("prodId")

	if prodId == "all":
		Product.objects.delete()
		return jsonify(success=True)
	else:
		# finds and deletes product after confirmation
		for product in Product.objects():
			targ = str(product.id)[-4:]
			if targ == prodId:
				product.delete()
				return jsonify(success=True)
		return jsonify(success=False, message="Invalid ID. Check inventory and make sure ID is correct.")

@app.route('/delete-recipe', methods=['POST'])
def deleteRecipe():
	''' deletes one or all recipes from database
	'''

	# immediately returns if no recipes in db
	if Recipe.objects.count() == 0:
		return jsonify(success=False, message="No recipes in database.")

	# select recipe and ensure it is in inventory
	rcpId = request.form.get("rcpId")

	if rcpId == "all":
		Recipe.objects.delete()
		return jsonify(success=True)
	else:
		# finds and deletes recipe after confirmation
		for recipe in Recipe.objects():
			targ = str(recipe.id)[-4:]
			if targ == rcpId:
				recipe.delete()
				return jsonify(success=True)
		return jsonify(success=False, message="Invalid ID. Check inventory and make sure ID is correct.")

if __name__ == "__main__":

	# license boilerplate
	print("GroceryHelper Copyright (C) 2019 Nathan Weinberg\nThis program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.\nThis is free software, and you are welcome to redistribute it\nunder certain conditions; type `show c' for details.\n")
	
	app.run(debug=True)
