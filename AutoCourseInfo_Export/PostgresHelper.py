import  sys
import  psycopg2
import configparser
config=configparser.ConfigParser()
config.read('webExtract.ini')
sys.path.append(config['ChoprasWebExtract']['custompythonpath'])
from   config   import  configDataBase

class   postgresHelper():
    def connect(self):
        try:
            params=configDataBase.config(self)
            self.connection=psycopg2.connect(**params)
            self.cursor=self.connection.cursor()            
            
        except (Exception, psycopg2.DatabaseError) as error:
            #To DO: Log the exception to database
            print("error")

    def closeConnection(self):
        try:
            if  self.connection is not None:
                self.connection.close()
            else:
                print("Connection is already closed")
        except (Exception, psycopg2.DatabaseError) as error:
            #To DO: Log the exception to database
            print("error")




