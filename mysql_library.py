import mysql.connector #pip install mysql-connector-python
import pandas as pd


class mysql_library(object):
    USERNAME = None
    PASSWORD = None
    HOST = None
    DATABASE = None
    PORT = None

    def __init__(self, username, password, host, database, port=3306):
        self.USERNAME = username
        self.PASSWORD = password
        self.HOST = host
        self.DATABASE = database
        self.PORT = port

    def execute_sql(self, query):
        '''
        Execute insert update delete query
        '''
        try:
            conn = mysql.connector.connect(user=self.USERNAME, password = self.PASSWORD, 
                                           host = self.HOST, database = self.DATABASE, port = self.PORT)
            cursor = conn.cursor()
            cursor.execute(query, multi=True)
            conn.commit()
        except Exception as ex:
            print(ex)
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def execute_sql_dataframe(self, query):
        '''
        Execute select query, return pandas data frame
        '''
        try:
            conn = mysql.connector.connect(user=self.USERNAME, password = self.PASSWORD, 
                                           host = self.HOST, database = self.DATABASE, port = self.PORT)
            cursor = conn.cursor()
            cursor.execute(query, multi=False)
            tableColumnNames = [i[0] for i in cursor.description]
            return pd.DataFrame(cursor.fetchall(), columns=tableColumnNames)
        except Exception as ex:
            print(ex)
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def execute_sql_schema(self, query):
        '''
        Execute schema change query
        '''
        try:
            conn = mysql.connector.connect(user=self.USERNAME, password = self.PASSWORD, 
                                           host = self.HOST, database = self.DATABASE, port = self.PORT)
            cursor = conn.cursor()
            cursor.execute(query)
        except Exception as ex:
            print(ex)
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def insert_df_into_table(self, dataframe, tableName):
        columnList = ['`' + column + '`' for column in dataframe.columns]
        columnListString = ','.join(columnList)
        values = []
        for i, r in dataframe.iterrows():
            row = []
            for value in r.values:
                if value == None:
                    v = 'NULL'
                else:
                    v = '"' + str(value).replace('"', '\\"') + '"'
                row.append(v)
            # row: ["DAL", "15, "6"]
            values.append('(' + ','.join(row) + ')')

        valuesString = ','.join(values)

        query = 'INSERT IGNORE INTO ' + tableName + ' (' + columnListString + ') VALUES ' + valuesString

        # print(query)
        self.execute_sql(query)

