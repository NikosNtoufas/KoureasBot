from telegram.ext import *
import telegram
from CONSTANTS import *
import sqlite3
import dbManager
import mainUtilities
from threading import Thread
from flashscoreScraper.dbManagerFlashscore import *
import flashscoreScraper.flashscore_scraper
import datetime

print("KoureasBot started...")

global updater

def sendMessageToAdmin(txt):
    bot = telegram.Bot(token=API_KEY)
    bot.send_message(chat_id=5079376391, text=txt)



def importantMatchesJob(context: telegram.ext.CallbackContext):
    matches = getImportantMatches("")
    nextMatches = [match for match in matches if mainUtilities.filterNext7Days(match[3])]

    if(len(nextMatches)>0):
        str = mainUtilities.getMatchesText(nextMatches)
        if len(str) > 4096:
            for user in dbManager.getUsers():
                for x in range(0, len(str), 4096):
                    context.bot.send_message(chat_id=user[0],text=str[x:x+4096],parse_mode=telegram.ParseMode.HTML)
        else:
            for user in dbManager.getUsers():
                context.bot.send_message(chat_id=user[0],text=str,parse_mode=telegram.ParseMode.HTML)

def matchesJob(context: telegram.ext.CallbackContext):
    matches = getAllMatches("")
    nextMatches = [match for match in matches if mainUtilities.filterNext7Days(match[3])]

    if(len(nextMatches)>0):
        str = mainUtilities.getMatchesText(nextMatches)
        if len(str) > 4096:
            for x in range(0, len(str), 4096):
                context.bot.send_message(chat_id=5079376391,text=str[x:x+4096],parse_mode=telegram.ParseMode.HTML)
        else:
            context.bot.send_message(chat_id=5079376391,text=str,parse_mode=telegram.ParseMode.HTML)


def start_command(update,context):
    if(dbManager.userExists(update.message.chat)):
        print(update.message.chat.id)
        update.message.reply_text("Hello " +update.message.chat.first_name)

def help_command(update,context):
    update.message.reply_text("help text")

def handle_message(update,context):
    if(not dbManager.userExists(update.message.chat)):
        update.message.reply_text("Anauthorized user")
        return
    
    text = update.message.text.lower()

#command for update flashscore data
    if(text =="update"):
        if(dbManager.isAdmin(update.message.chat)):
            Thread(target=flashscoreScraper.flashscore_scraper.run).start()
            update.message.reply_text("update started...")
            return
        else:
            update.message.reply_text("unauthorized for this command")
            return


    arr =text.split(" ")



    team = mainUtilities.getTeam(arr)
    if(team==""):
        update.message.reply_text("no team detected")
        return 
    
    if(mainUtilities.isProgramComand(arr)):    
        matches = getImportantMatches(team) if mainUtilities.isImportantCommand(arr) else getAllMatches(team)
        str = mainUtilities.getMatchesText(matches)
        if len(str) > 4096:
            for x in range(0, len(str), 4096):
                 update.message.bot.send_message(chat_id=update.message.chat.id,text=str[x:x+4096],parse_mode=telegram.ParseMode.HTML)
        else:
            update.message.bot.send_message(chat_id=update.message.chat.id,text=str,parse_mode=telegram.ParseMode.HTML)
        return



    city = mainUtilities.getCity(arr)

    if(city==""):
        path = BASE_PATH + '/'+ team + '/'+ city
         
        list = mainUtilities.getSubFolders(path)
        if(len(list)==0):
            update.message.bot.send_message(update.message.chat.id,"no persons data for " + team + "," + city)
            return
        str = "\n".join(list)

        #GET AVAILABLE CITIES
        update.message.bot.send_message(chat_id=update.message.chat.id,text=str,parse_mode=telegram.ParseMode.MARKDOWN)
        
        return
    
  


    path = BASE_PATH + '/'+ team + '/'+ city

    person_name = ''
    

    if(len(arr)==0):
        #send all city photos
        images = mainUtilities.getImagesOfFolder(path)
        if(len(images)==0):
            update.message.bot.send_message(update.message.chat.id,"no data")
            return
        for i in images:
            update.message.bot.send_photo(update.message.chat.id,i)

        return
    


    if(len(arr)>0):
        if arr[0] == "cars":
            #get all available cars of city
            cars = mainUtilities.getAllCars(path)
            str = "\n".join(cars)
            update.message.bot.send_message(chat_id=update.message.chat.id,text=str,parse_mode=telegram.ParseMode.MARKDOWN)
            return
        elif(arr[0] == "list"):
            #get list of persons of city
            list = mainUtilities.getSubFolders(path)
            str = "\n".join(list)
            if(len(list)==0):
                update.message.bot.send_message(update.message.chat.id,"no persons data for " + team + "," + city)
                return

            images = mainUtilities.getOnlyListImagesPath(path,list)
            for i in images:
                t= images[i]
                caption = mainUtilities.getInfo(path+"/"+i)
                if(caption==""):
                    caption = i
                update.message.bot.send_photo(update.message.chat.id,open(t,'rb'),caption=caption)
            return
        else:
            person_name = ' '.join(arr).lower()
            path+= "/"+ '_'.join(arr).lower()
            images = mainUtilities.getImagesOfFolder(path)
            if(len(images)==0):
                update.message.bot.send_message(update.message.chat.id,"no data")
                return

            #add caption
            if(person_name!=''):
                images[0].caption = person_name
            

            update.message.bot.send_media_group(update.message.chat.id,images)
            return

       

def main():
    updater = Updater(API_KEY,use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start",start_command))
    dp.add_handler(CommandHandler("help",help_command))
    dp.add_handler(MessageHandler(Filters.text,handle_message))

    j = updater.job_queue
    j.run_repeating(importantMatchesJob, interval=259200, first=10)
    t = datetime.time(hour=12, minute=00, second=00)
    j.run_daily(matchesJob, t, days=tuple(range(1)))

    updater.start_polling(5)
    updater.idle()
  
if __name__ == '__main__':
    main()
  

