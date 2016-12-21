import os
import re
import sys
import subprocess

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
    ngram="ngram"
    order = "2"

    texts=GetTextFiles("/home/rottik/detekce/detekce_tematu/CZ",".lm"+order)

#./ngram-count -text ~/detekce/detekce_tematu/CZ.texts -order 3 -write CZ.model3

    results={}
    for topic_text in texts:
        command = srilm_bin+ngram+" -lm "+topic_text+" -ppl "+sys.argv[0]
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        match = re.search("logprob=\s*(-?\d+\.\d*)\s", str(output))
        res = float(match.group(1))
        results[topic_text]=res;
        #os.system( command );
    for w in sorted(results, key=results.get, reverse=True):
        print(w, results[w])
    
