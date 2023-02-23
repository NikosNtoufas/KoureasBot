import dbManager
import os
from telegram import InputMediaPhoto
from fnmatch import fnmatch
import pathlib
from pathlib import Path

def getTeam(arr):
    for x in arr:
        t = dbManager.getTeam(x.lower())
        if(t!=""):
            arr.remove(x)
            return t
    return ""

def getCity(arr):
    for x in arr:
        t = dbManager.getCity(x.lower())
        if(t!=""):
            arr.remove(x)
            return t
            
    return ""


def getImagesOfFolder(path):   
    imgs =  []
    if(not Path(path).exists()):
        return imgs
    valid_images = [".jpg",".gif",".png",".tga"]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        imgs.append(InputMediaPhoto(open(path+'/'+f,'rb')))
    return imgs

def getOnlyListImagesPath(path,list):
    dict =  {}
    if(not Path(path).exists()):
        return 
    for l in list:
        p = path+'/'+l
        valid_images = [".jpg",".gif",".png",".tga"]
        for f in os.listdir(p):
            ext = os.path.splitext(f)[1]
            if(f.rsplit('.', 1)[0]!='1'):
                continue
            if ext.lower() not in valid_images:
                continue
            dict[l]=p+'/'+f
        
    return dict

def getAllCars(path):
    cars = []
    if(not Path(path).exists()):
        return cars

    for root, subdirs, files in os.walk(path):
        for name in files:
            if name=="car.txt":
                filepath = os.path.join(root,name)
                file = open(filepath, encoding="utf8")
                data = file.read()
                file.close()
                cars.append(pathlib.PurePath(root).name+": " + data)

    return cars

def getListOfPersons(path):
    sub_folders = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    return sub_folders


def isProgramComand(arr):
    list = ["προγραμμα","πρόγραμμα" ,"προγραμα","προγραμα","programma","programa" ]
    for x in arr:
        if x.lower() in list:
            return True

    return False

def isImportantCommand(arr):
    list = ["!","*","important"]
    for x in arr:
        if x.lower() in list:
            return True


def getMatchesText(matches):
    str = ""
    header1 = ""
    header2 = ""
    for m in matches:
        if(m[5]!=header1):
           
            header1=m[5]

            str += "\n\n<b>\t-------"+header1+"-------</b> \n" 

            if(m[6]!=header2):
                header2=m[6]
                
                str += "\n<u>"+header2+"</u>" 
                
        if(m[6]!=header2):
            if(header2!=""):
                str+="----------------------------------------------\n"
            header2=m[6]
            
            str += "\n<u>"+header2+"</u>" 

        if(m[7]=="very high"):
            str+="\n<b><i>"+ m[3]+ " " + m[4] +" "+ m[1] + " vs "+ m[2]+"</i></b>❗"+"\n"
        elif(m[7]=="high"):
            str+="\n<i>"+ m[3]+ " " + m[4] +" "+ m[1] + " vs "+ m[2]+"</i>✈"+"\n"   
        elif(m[7]=="medium"):
            str+="\n<b>"+ m[3]+ " " + m[4] +" "+ m[1] + " vs "+ m[2]+"</b>"+"\n"   
        else: 
            str+="\n"+m[3]+ " " + m[4] +" " + m[1] + " vs "+ m[2]+"\n"

    return str