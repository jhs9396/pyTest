import sys
import os
import codecs

def writeCSV(filePath,header,results):
    try:
        import unicodecsv
    except ImportError:
        print("[+] Install the unicodecsv module to write the CSV report")
        sys.exit(1)

    with open(os.path.join(filePath), "wb") as csvfile:
        writer = unicodecsv.writer(csvfile, delimiter=',', encoding='utf-8')
        writer.writerow(header)
        for row in results:
            writer.writerow(list(row))
            
def get_stop_words(filePath):
    with codecs.open(os.path.join(filePath)) as f:
        stopSet = set()
        
        for line in f:
            stopSet.add(line)

        return frozenset(stopSet) 