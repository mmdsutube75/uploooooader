import mysql.connector

class Database:
    def __init__(self, user , password , databaseName) -> None:
        self.db = mysql.connector.connect(
            host = "localhost",
            user = user,
            password = password,
            auth_plugin = "mysql_native_password",
            database = databaseName,
        )

        self.cursor = self.db.cursor()

    def createTable(self):
        self.cursor.execute(
                "create table file_ids(file_unique_id VARCHAR(255) , file_id VARCHAR(255));"
            )
        self.cursor.execute(
                "create table users_data(userid VARCHAR(255) , username VARCHAR(255))"
            )
    def insertFileIdToDb(self , fileUniqeId , fileId):
        self.db.connect()
        sql = "insert into file_ids (file_unique_id , file_id) values (%s , %s)"
        val = (fileUniqeId , fileId)
        self.cursor.execute(sql , val)
        self.db.commit()

    def fileIdExist(self,fileUniqeId ):
        self.db.connect()
        sql = f"select file_id from file_ids where file_unique_id = '{fileUniqeId}'"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if(result):
            return result[0]
        return(None)
    
    def checkUserExist(self , userId : int | str):
        self.db.connect()
        sql = f"select userid from users_data where userid = '{userId}' "
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        # print(result)
        if(result):
            return True
        else:
            return False
    def insertUserInfToDb(self , userid : int | str , username):
        self.db.connect()
        sql = "insert into users_data (userid , username) values (%s , %s)"
        val = (userid , username)
        self.cursor.execute(sql , val)
        self.db.commit()
        
    def showAllRecord(self , tableNmae):
        self.db.connect()
        self.cursor.execute(f"select * from {tableNmae};")
        return(self.cursor.fetchall())

# created by @abdollahi4730