import sqlite3 
import sys
sys.path.append("flashscoreScraper")
import CONSTANTS_FLASHSCORE


def clearMatches(sport,competition):

    try:
        sqliteConnection = sqlite3.connect('flashscoreMatches.db')


        par = (str(sport),str(competition))
          
        sql = ''' delete from matches where sport = ? and competition = ? '''

        cursor = sqliteConnection.cursor()
        cursor.execute(sql,par)
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Error on deleting rows ", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


def insertMatches(matches):
    try:
        sqliteConnection = sqlite3.connect('flashscoreMatches.db')
        
        sql = ''' insert into matches(id,homeTeam,awayTeam,date,time,sport,competition,importance)
              VALUES(?,?,?,?,?,?,?,?) '''

        cursor = sqliteConnection.cursor()
       
        for match in matches:
            matchDb = (str(match.id[0]),str(match.homeTeam),str(match.awayTeam),
            str(match.date),str(match.time),str(match.sport),str(match.competition),str(match.importance))
            cursor.execute(sql,matchDb)
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

    return


def getAllMatches(team):
    try:
        sqliteConnection = sqlite3.connect('flashscoreMatches.db')
        
        par = (str(CONSTANTS_FLASHSCORE.FLASHSCORE_MAIN_TEAMS[team]),str(CONSTANTS_FLASHSCORE.FLASHSCORE_MAIN_TEAMS[team]))
        if(team==""):
            sql = ''' select * from matches where() homeTeam=? or awayTeam=? ) '''
        else:
            sql = ''' select * from matches where homeTeam=? or awayTeam=? '''

        cursor = sqliteConnection.cursor()
       
        cursor.execute(sql,par)
        matches = cursor.fetchall()

        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

    return matches

def getImportantMatches(team):
    try:
        sqliteConnection = sqlite3.connect('flashscoreMatches.db')
        
        par = (str(CONSTANTS_FLASHSCORE.FLASHSCORE_MAIN_TEAMS[team]),str(CONSTANTS_FLASHSCORE.FLASHSCORE_MAIN_TEAMS[team]),"very high","high")
        if(team==""):
            sql = ''' select * from matches where (importance=? or importance =?)'''
        else:
            sql = ''' select * from matches where (homeTeam=? or awayTeam=?) and (importance=? or importance =?) '''

        cursor = sqliteConnection.cursor()
       
        cursor.execute(sql,par)
        matches = cursor.fetchall()

        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

    return matches