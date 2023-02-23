from telegram.ext import *
import telegram
from CONSTANTS import *
import sqlite3
import dbManager
import mainUtilities
import flashscoreScraper.dbManagerFlashscore


print("KoureasBot started...")


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
    
    text = update.message.text
    arr =text.split(" ")



    team = mainUtilities.getTeam(arr)
    if(team==""):
        update.message.reply_text("no team detected")
        return 
    
    if(mainUtilities.isProgramComand(arr)):    
        matches = flashscoreScraper.dbManagerFlashscore.getImportantMatches(team) if mainUtilities.isImportantCommand(arr) else flashscoreScraper.dbManagerFlashscore.getAllMatches(team)
        str = mainUtilities.getMatchesText(matches)
        update.message.bot.send_message(chat_id=update.message.chat.id,text=str,parse_mode=telegram.ParseMode.HTML)
        return



    city = mainUtilities.getCity(arr)

    if(city==""):
        update.message.reply_text("no city detected")
        return
    
  


    path = BASE_PATH + '/'+ team + '/'+ city

    person_name = ''
    if(len(arr)>0):
        if arr[0] == "cars":
            cars = mainUtilities.getAllCars(path)
            str = "\n".join(cars)
            update.message.bot.send_message(chat_id=update.message.chat.id,text=str,parse_mode=telegram.ParseMode.MARKDOWN)
            return
        elif(arr[0] == "list"):
            list = mainUtilities.getListOfPersons(path)
            str = "\n".join(list)
            if(len(list)==0):
                update.message.bot.send_message(update.message.chat.id,"no persons data for " + team + "," + city)
                return

            images = mainUtilities.getOnlyListImagesPath(path,list)
            for i in images:
                t= images[i]
                update.message.bot.send_photo(update.message.chat.id,open(t,'rb'),caption=i.replace('_',' '))
            return


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

    updater.start_polling(5)
    updater.idle()

    
if __name__ == '__main__':
    main()