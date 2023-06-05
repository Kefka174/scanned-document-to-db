import mysql.connector
from mysql.connector import errorcode

class MySQLConnector():
    defaultConfig = {
        "host": "localhost",
        "user": "root",
        "password": "toor",
        "database": "yacht_club"
    }
    
    def __init__(self, config = defaultConfig):
        self.config = config
        self.connect()

    def connect(self):
        try:
            self.db = mysql.connector.connect(**self.config)
            self.cursor = self.db.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Incorrect username or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def close(self):
        self.cursor.close()
        self.db.close()

    def getTables(self):
        print("TODO: return tables and fields in database")
        # query for tables
        # for each table: query for fields
        # don't show foreign keys
        # sort by foreign keys

    def insert(self, valuesDict):
        print("TODO: insert values from dict to db")
        # store foreign keys
        # for table in valuesDict:
            # for field in table:



if __name__ == '__main__':
    connector = MySQLConnector()
    connector.close()