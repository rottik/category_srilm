#!/usr/bin/python3.5
'''
Converts text to UTF-8
removes mateinformation

'''
import codecs
import os
import sys

def GetTextFiles(rootDir, pattern):
    import os
    import os.path
    files=[]
    for dirpath, dirnames, filenames in os.walk(rootDir):
        for filename in [f for f in filenames if f.endswith(pattern)]:
            files.append( os.path.join(dirpath, filename))
    return files
    
def remove_metadata(text):
    import re
    metaline_regex = re.compile("^.*\\|.*$")
    lines=text.splitlines()
    newlines=[]
    for line in lines:
        if(line.strip()=="------------------"):
            continue
        if(metaline_regex.match(line)):
            continue
        newlines.append(line)
    
    return "\r\n".join(newlines)
    

if __name__ == "__main__":
    directory="PL"
    chybne=0
    counter=0
    files = GetTextFiles(directory,".txt")
    for f in files:
        try:
            counter+=1
            if(os.path.isfile(f+".clean")):
                continue
            FR = codecs.open(f,"r",'windows-1250')
            text = FR.read()
            FR.close()
            FW = codecs.open(f+".clean","w")
            FW.write(remove_metadata(text))
            FW.close()
            if(counter%1000==0):
                print("hotovo:"+str(counter)+" "+str((counter*100)/len(files))+" %")
        except UnicodeDecodeError:
            chybne+=1
    print("Chybne soubory:" +str(chybne))
    files = GetTextFiles(directory,".txt.clean")
    counter=0
    for f in files:
        counter+=1
        if(counter%1000==0):
            print("hotovo:"+str(counter)+" "+str((counter*100)/len(files))+" %")
        if(os.path.isfile(f.replace(".clean",".token"))):
            continue
        os.system("python unitok.py -n < "+f+" > "+f.replace(".clean",".token"))  
    
