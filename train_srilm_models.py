import os

def GetTextFiles(rootDir, pattern):
    import os
    import os.path
    files=[]
    for dirpath, dirnames, filenames in os.walk(rootDir):
        for filename in [f for f in filenames if f.endswith(pattern)]:
            files.append( os.path.join(dirpath, filename))
    return files

if __name__ == "__main__":
    srilm_bin="/home/rottik/srilm/bin/i686-m64/"
    ngram_count="ngram-count"
    order = "10"

    texts=GetTextFiles("/home/rottik/detekce/detekce_tematu/myCZ",".train")

#./ngram-count -text ~/detekce/detekce_tematu/CZ.texts -order 3 -write CZ.model3

    for topic_text in texts:
        print("training:" +topic_text+".model"+order)
        #os.system(srilm_bin+ngram_count+" -text "+topic_text+" -order "+order +" -addsmooth 1 -lm "+topic_text+".lm"+order);
        os.system(srilm_bin+ngram_count+" -text "+topic_text+" -order "+order +" -wbdiscount "+order+" -lm "+topic_text+".lm"+order+"wb"+order);
        #~/srilm/bin/i686-m64/ngram-count -text CZ/ekonomika.train -order 3  -lm CZ/ekonomika.train.lm3.wb3
