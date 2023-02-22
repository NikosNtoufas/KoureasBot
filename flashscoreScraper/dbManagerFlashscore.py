import sqlite3

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