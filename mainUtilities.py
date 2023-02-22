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
