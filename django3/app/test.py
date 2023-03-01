

import mysql.connector
from mysql.connector import errorcode

class DAO():
    def __init__(self, table):
        self.args = {
            'host':'db',
            'user':'user',
            'password':'passw0rd',
            'database':'stock_database',
            "charset":'utf8'
        }
        self.config = self.args.copy()
        self.config.update({
            "table" : table
        })
        self.conn = None
        self.cursor = None
    
    def run(self, cmd):
        # Drop previous table of same name if one exists
        #self.cursor.execute("DROP TABLE IF EXISTS inventory;")
        #print("Finished dropping table (if existed).")
        self.cursor.execute(cmd)
        return self.cursor.fetchall()

    def select_all(self):
        self.cursor.execute('SELECT * FROM {}.{}'.format( self.config["database"] , self.config["table"]) )
        return self.cursor.fetchall()

    def __enter__(self):
        try:
            self.conn = mysql.connector.connect(**self.args)
        except mysql.connector.Error as err:
            raise err
        else:
            self.cursor = self.conn.cursor(dictionary=True)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()



with DAO("test") as dao:
    print("hello")
    dao.run("CREATE TABLE CardInfo ( CardID nchar(6),. CustomerID nchar(5), IssueDate datetime, ExpireDate datetime, EmployeeID int)")



