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
    lang="PL"
    extension = ".token"
    themesFiles=os.listdir(lang)
    themes=[]
    print("Temat:" +str(len(themes)))
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
    for theme in themes:
        trainY.extend(train*[theme])
        valY.extend(valid*[theme])
        testY.extend(test*[theme])
    
    for theme in themes:
        trainX.append(dic[theme][0:train])
        valX.append(dic[theme][train:train+valid])
        testX.append(dic[theme][-test:-1])
    
    pickle.dump(trainX,open(lang+"/paths_trainX.pcl","wb"))
    pickle.dump(trainY,open(lang+"/labels_trainY.pcl","wb"))
    pickle.dump(valX,open(lang+"/paths_valX.pcl","wb"))
    pickle.dump(valY,open(lang+"/labels_valY.pcl","wb"))
    pickle.dump(testX,open(lang+"/paths_testX.pcl","wb"))
    pickle.dump(testY,open(lang+"/labels_testY.pcl","wb"))
    
    trainData = []
    AllTexts=[]
    labels=[]
    for i in range(len(trainX)):
        for x in trainX[i]:
            FR = open(x,'r')
            text=FR.read()
            FR.close()
            AllTexts.append(text)
            labels.append(themes[i])
            trainData.append(text)
    
    pickle.dump(trainData,open(lang+"/texts_train.pcl",'wb'))
    
    valData = []
    for i in range(len(valX)):
        for x in valX[i]:
            FR = open(x,'r')
            text=FR.read()
            FR.close()
            AllTexts.append(text)
            labels.append(themes[i])
            valData.append(text)    
    pickle.dump(valData,open(lang+"/texts_val.pcl",'wb'))
    
    testData = []
    for i in range(len(testX)):
        for x in [y for y in testX[i]]:
            FR = open(x,'r')
            text=FR.read()
            FR.close()
            AllTexts.append(text)
            labels.append(themes[i])
            testData.append(text)
    pickle.dump(labels,open(lang+"/labels.pcl","wb"),protocol=2)
    pickle.dump(AllTexts,open(lang+"/texts.pcl","wb"),protocol=2)
    pickle.dump(testData,open(lang+"/texts_test.pcl",'wb'))
    
    
