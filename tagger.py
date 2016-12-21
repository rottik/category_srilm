'''
    Classification server
    args: tagger_file rnn_model_file
'''

import pickle
import socket
import time
import sys
#from thread import *
import os
import os.path
import codecs
from random import shuffle
import numpy as np
from ufal.morphodita import *


######################################################################################################
# metody
    
def encode_entities(text):
  return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    
def LemmatizeText(text):
    formsMorp = Forms()
    lemmasMorp = TaggedLemmas()
    tokensMorp = TokenRanges()
    tokenizerMorp = taggerMorp.newTokenizer()
    if tokenizerMorp is None:
        sys.stderr.write("No tokenizer is defined for the supplied model!")
        sys.exit(1)
        
    tokenizerMorp.setText(text)
    lemmatizedText="";
    while tokenizerMorp.nextSentence(formsMorp, tokensMorp):
        taggerMorp.tag(formsMorp, lemmasMorp)
        for i in range(len(lemmasMorp)):
            lemmaMorp = lemmasMorp[i]
            lemmatizedText+=encode_entities(lemmaMorp.lemma.split("_")[0].split("-")[0])+" "
    lemmatizedText = lemmatizedText.strip()
    return lemmatizedText
    
def GetTextFiles(rootDir, pattern):
    import os
    import os.path
    files=[]
    for dirpath, dirnames, filenames in os.walk(rootDir):
        for filename in [f for f in filenames if f.endswith(pattern)]:
            files.append( os.path.join(dirpath, filename))
    return files
    
##########################################################################################################
# inicializace 

# NACIST MORPHODITU
print( "Loading tagger...")
taggerMorp = Tagger.load(sys.argv[1])
if not taggerMorp:
    sys.stderr.write("Cannot load tagger from file '%s'\n" % sys.argv[1])
    sys.exit(1)
print( "Tagger loaded.")
deleted=0
deletedFiles=[]
files = list(set(GetTextFiles("CZ1",".txt")) | set(GetTextFiles("CZ2",".txt")))
num_of_files=len(files)
counter=0
print(len(files))
for fil in files:
    if(os.path.exists(fil+".lemma")):
        continue
    try:
        counter+=1
        if(counter%500==0):
            print("proccessed:"+str(counter)+" files ("+str(counter*100/num_of_files)+" %)")
        #print(fil)
        FR = codecs.open(fil,"r",'windows-1250')
        text = FR.read()
        FR.close()
        FW = codecs.open(fil+".lemma","w")
        FW.write(LemmatizeText(text))
        FW.close()
    except UnicodeDecodeError:
        deletedFiles.append(fil)
        deleted+=1
        os.remove(fil)
        print("Files deleted:"+str(deleted))
