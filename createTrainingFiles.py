#!/usr/bin/python3.5
import os
import pickle
import math
from random import shuffle

def GetTextFiles(rootDir, pattern):
    import os
    import os.path
    files=[]
    for dirpath, dirnames, filenames in os.walk(rootDir):
        for filename in [f for f in filenames if f.endswith(pattern)]:
            files.append( os.path.join(dirpath, filename))
    return files


if __name__ == "__main__":
    lang="CZ"
    extension = ".lemma"
    themesFiles=os.listdir(lang)
    themes=[]
    dic={}
    for theme in themesFiles:
        if(os.path.isdir(lang+"/"+theme)):
            themes.append(theme)
            print(theme)
            files = GetTextFiles(lang+"/"+theme,extension)
            shuffle(files)
            dic[theme]=files
            print(len(files))
        
    # limit je x tisic souboru - nejmensi spolecny pocet
    limit = math.floor(min([len(val) for val in dic.values()])/1000)*1000
    
    #80 % trenovaci, 10 % ladici, 10 % testovaci
    trainX=[]
    trainY=[]
    valX=[]
    valY=[]
    testX=[]
    testY=[]
    
    train = int(math.floor(limit*0.8))
    valid= int(math.floor(limit*0.1))
    test = int(math.floor(limit*0.1))
    
    #trainX.append(dic[theme][0:train])
    #valX.append(dic[theme][train:train+valid])
    #testX.append(dic[theme][-test:-1])
    
    for theme in themes:
        print("creating file: "+lang+"/"+theme+".train")
        tw = open(lang+"/"+theme+".train","w")
        for train_file in dic[theme][0:train]:
            tr = open(train_file,"r")
            content = tr.read()
            tr.close()
            tw.write(content+"\n")
        tw.close()
        print("creating file: "+lang+"/"+theme+".val")
        tw = open(lang+"/"+theme+".val","w")
        for train_file in dic[theme][train:train+valid]:
            tr = open(train_file,"r")
            content = tr.read()
            tr.close()
            tw.write(content+"\n")
        tw.close()
        print("creating file: "+lang+"/"+theme+".test")
        tw = open(lang+"/"+theme+".test","w")
        for train_file in dic[theme][-test:-1]:
            tr = open(train_file,"r")
            content = tr.read()
            tr.close()
            tw.write(content+"\n")
        tw.close()
