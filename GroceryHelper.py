'''
GroceryHelper: A simple text-based program designed to help users keep track of their groceries
Copyright (C) 2017 Nathan Weinberg

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

# imports
import shelve
import datetime

# colors text in Windows command prompt
from colorama import init, Fore, Back, Style
init()

# opens shelf file and computes current date
shelfFile = shelve.open('inventory')
currentDate = datetime.datetime.today()

# Class/Function Definitions
class Product:
    def __init__(self, name, expDate):
        self.name = name
        self.expDate = expDate
        self.quantity = 1

    def __repr__(self):
        return self.name + ": Expires " + str(self.expDate)

    def isExpired(self):
        if self.expDate < currentDate:
            return True

def displayInventory(productList):
    ''' Displays all items currently in inventory, as well as total size
        If item is expired item will print in red
    '''
    for product in productList:
        if product.isExpired():
            print(Fore.RED + str(product))
            print(Style.RESET_ALL, end='')
        else:    
            print(product)
    print("Total number of items: " + str(len(productList)))

def inputProduct(productList):
    ''' takes in a product name and expiration date
        and generates a new Product object in inventory
        also sorts inventory
    '''

    # item creation code
    while True:
        try:

            # get product name
            name = str(input("Please input product name: "))

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
            break

        # Loops if user input data incorrectly, causing strptime to throw a ValueError
        except ValueError:
            print('\nPlease enter all fields in the correct format\n')

    # Creates new Product object and adjusts quantities accordingly
    newProduct = Product(name, expDateClass)
    # quantity code
    for item in productList:
        if item.name == newProduct.name:
            item.quantity += 1
            newProduct.name += '('+ str(item.quantity) + ')'
            newProduct.quantity += 1

    # Adds new Product object to list of products
    productList += [newProduct]
    # Sorts list
    productList.sort(key=lambda product: product.name)

def deleteProduct(productList):
    ''' deletes one or all items from inventory
    '''

    # select product and ensure it is in inventory
    product = str(input('Please input the name of the product you wish to remove, or input "All" to empty inventory: '))
    
    # if "All"
    if product.lower() == "all":
        while True:
            deleteConfirmAll = str(input("Are you sure you wish to delete all products from your inventory? Y/N ")).lower()
            if deleteConfirmAll == 'y':
                del productList[:]
                break
            elif deleteConfirmAll == 'n':
                break
            else:
                print('\nInvalid choice. Please try again.')

    # else
    else:

        # finds and deletes product after confirmation
        for item in productList:
            if item.name == product:

                while True:
                    deleteConfirm = str(input("Are you sure you wish to delete " + product + " from your inventory? Y/N ")).lower()
                    if deleteConfirm == 'y':
                        productList.remove(item)
                        return
                    elif deleteConfirm == 'n':
                        return
                    else:
                        print('\nInvalid choice. Please try again.')

        print("Invalid product. Check inventory and make sure name is correct.")

def checkExpired(productList):

    # scans through all products
    for product in productList:

        # if product is expired, alert user and prompt if they wish to delete it from inventory
        if product.isExpired():

            while True:
                choice = str(input(product.name + ' has expired. Do you wish to delete it from your inventory? Y/N ')).lower()
                # NOTE: Cannot delete from productList directly due to nested for loop; instead stores product in delQueue
                if choice == 'y':
                    productList.remove(product)
                    break
                elif choice == 'n':
                    break
                else:
                    print('\nInvalid choice. Please try again.')

# Main function
def main():

    print("GroceryHelper Copyright (C) 2017 Nathan Weinberg\nThis program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.\nThis is free software, and you are welcome to redistribute it\nunder certain conditions; type `show c' for details.")


    # Imports data from shelfFile; if none exists creates new list
    try:
        productList = shelfFile['productList']
    except:
        productList = []

    # checks if any products have expired 
    checkExpired(productList)
    
    while True:

        # Display        
        print("\n-------------------------------------------\n               GroceryHelper\nCurrent Date is: " + str(currentDate) + "\n-------------------------------------------")
        print("(1) Display inventory")
        print("(2) Input new product")
        print("(3) Delete product")
        print("(0) Exit Program\n")

        # scan for user choice
        choice = input("Make a selection: ")

        # ensure choice is type int
        try:
            choice = int(choice)
        except ValueError:
            print("\nPlease input a number.")
        else:
            # Display inventory
            if choice == 1:
                displayInventory(productList)
            # Input new product
            elif choice == 2:
                inputProduct(productList)               
            # Delete product
            elif choice == 3:
                deleteProduct(productList)
            # Exit
            elif choice == 0:
                break
            # Invalid choice
            else:
                print('\nInvalid choice. Please try again.\n')

    # Saves shelf file and exits program
    shelfFile['productList'] = productList
    shelfFile.close()
    print("\nGoodbye!")

# More client code
if __name__ == "__main__":
    main()
