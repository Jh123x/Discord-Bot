import sqlite3

class DB:
    def __init__(self):
        #The initialiser for the database class
        self.conn = sqlite3.connect('economy.db')
        self.cursor = sqlite3.Cursor()
    
    def add(self, name):
        #Adds a new user to the database
        pass

    def update(self, name, amount):
        #Update the amount of money a use has in the server
        pass

    def remove(self, name):
        #Remove the user from the economy
        pass

    def reset(self, name):
        #Reset the amount of money the user has in the server
        pass
        
