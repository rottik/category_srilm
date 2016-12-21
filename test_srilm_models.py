import os
import locale
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
import io
import re
import subprocess
import sys
from nltk import word_tokenize

srilm_bin="/home/rottik/srilm/bin/i686-m64/"
ngram="ngram"

def GetTextFiles(rootDir, pattern):
    import os
    import os.path
    files=[]
    for dirpath, dirnames, filenames in os.walk(rootDir):
        for filename in [f for f in filenames if f.endswith(pattern)]:
            files.append( os.path.join(dirpath, filename))
    return files

def CatMultiArticleFile(filename, model):
    command = srilm_bin+ngram+" -lm "+model+" -ppl temp.txt -debug 1"
    #print(command+"<br/>")
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    matches = re.findall("logprob=\s*(-?\d+\.\d*)\s", str(output))
    res=[]
    for match in matches:
        res.append(float(match))
    return res

def CatProb(text,model):
    tokens = " ".join(word_tokenize(text))
    fw=open("temp.txt",'w')
    fw.write(tokens)
    fw.close()
    #print(model)
    command = srilm_bin+ngram+" -lm "+model+" -ppl temp.txt"
    #print(command+"<br/>")
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    match = re.search("logprob=\s*(-?\d+\.\d*)\s", str(output))
    res = float(match.group(1))
    return res
    
def FindBestCats(text, model_dir, model_type):
    probs={}
    models = GetTextFiles(model_dir, model_type)
    for model in models:
        probs[model]=CatProb(text,model)
    result=""
    max_value=float("-inf")
    for w in sorted(probs, key=probs.get, reverse=True):
        if(max_value<=probs[w]):
            max_value=probs[w]
            result+=w+" "    
    return result.strip()

def CreateCategoryFile(filename, model_dir, model_type):
    lines = [line.rstrip('\n') for line in open(filename)]
    print("lines:"+str(len(lines)))
    err_counter=0
    if(os.path.exists(filename+model_type+".res")):
        return
    fw=open(filename+model_type+".res", 'w')
    cnt=0;
    for line in lines:
        try:
            cnt+=1
            fw.write(FindBestCats(line, model_dir, model_type))
        except AttributeError:
            print("-------- ERROR --------", end=" ")
            #print(line)
            err_counter+=1
        if(cnt%10==0):
            print(cnt, end=" ")
    fw.close()
    print("\n"+filename+"\t"+str(err_counter))
    
def CreateCategoryFileByLines(filename, model_dir, model_type):
    probs={}
    models = GetTextFiles(model_dir, model_type)
    counter=0;
    for model in models:
        probs[model]=CatMultiArticleFile(filename, model)
        counter = len(probs[model]);
    results=[]
    print( counter)
    for index in range(0,counter-1):
        m=999
        cat=0
        for model in models:
            if(m>probs[model][index]):
                m=probs[model][index]
                cat=model
        print(cat)
        results.append(cat+" ")
    fw=open(filename+model_type+".res", 'w')
    for res in results:
        fw.write(res)
    fw.close()
    
model_dir="CZ";
model_type=".lm10wb10";
data_dir="CZ"
print(model_type)

testfiles = GetTextFiles(data_dir,".test")

print(testfiles)
for test_file in testfiles:
    print(test_file)
    CreateCategoryFile(test_file, model_dir, model_type)
    

