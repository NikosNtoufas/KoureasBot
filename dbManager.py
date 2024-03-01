import sqlite3
from CONSTANTS import ADMIN_ID


def isAdmin(chat):
    if(chat.id==ADMIN_ID):
        return True
    return False

def getUsers():
    try:
        sqliteConnection = sqlite3.connect('valantisBot.db')
        cursor = sqliteConnection.cursor()
        cursor.execute('select * from users where active==1')
        users = cursor.fetchall()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
    return users


def userExists(chat):
    exist= False
    try:
        sqliteConnection = sqlite3.connect('valantisBot.db')
        cursor = sqliteConnection.cursor()
        cursor.execute('select * from users where id like ' + str(chat.id))
        user = cursor.fetchone()
        if user!=None:
            print(str(chat.id) + ' found')

            if(user[3]==1):
                exist = True
            else:
                print(str(chat.id) + ' need authoriziation')
        else:
            print(str(chat.id) + ' user not found')
            createUser(chat)

        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

    return exist


def createUser(chat):
    try:
        sqliteConnection = sqlite3.connect('valantisBot.db')

        sql = ''' insert into users(id,team_id,username,active)
              VALUES(?,?,?,?) '''

        cursor = sqliteConnection.cursor()
        user = (str(chat.id),0,str(chat.first_name),0)
        cursor.execute(sql,user)
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

    return

def getCity(text):
    try:
        sqliteConnection = sqlite3.connect('valantisBot.db')
        cursor = sqliteConnection.cursor()
        cityId=0
        cityname = ""

        cursor.execute("select city_id from cities_naming where name_text like '" + str(text)+"'")
        cityId = int(cursor.fetchone()[0])
        if(cityId==0):
            return ""

        cursor.execute("select name from cities where id = "+ str(cityId))
        cityname = cursor.fetchone()[0]

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        return ""
    finally:
        cursor.close()
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        return cityname

def getTeam(text):
    try:
        sqliteConnection = sqlite3.connect('valantisBot.db')
        cursor = sqliteConnection.cursor()
        teamId=0
        teamname=""

        cursor.execute("select team_id from teams_naming where name_text like '" + str(text)+"'")
        teamId = int(cursor.fetchone()[0])
        if(teamId==0):
            return ""

        cursor.execute("select name from teams where id = "+ str(teamId))
        teamname = cursor.fetchone()[0]

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        return ""
    finally:
        cursor.close()
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        return teamname



