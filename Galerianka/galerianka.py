import os
from shutil import copy2
import random as r

with open("index.txt", "w", encoding="utf-8") as f:
    for _ in range (1600):
        randomid = r.randint(1,2000)
        f.write(str(randomid) + "\n")

def indexFiles():
    src = "C:\\Users\\Mateusz\\Desktop\\galeria\\toindex\\"
    dest = "C:\\Users\\Mateusz\\Desktop\\galeria\\indexed\\"
    files = os.listdir(src)
    index = 1 
    for file in files:
        if file.endswith(".jpg") or file.endswith(".png"):
            newFile = str(index) + ".jpg" 
            srcFile = src+file
            destFile = dest+newFile
            print(srcFile + " " + destFile)
            copy2(srcFile, destFile)
            index +=1
        
def deleteChosenFiles():
    indexFiles()    
    dest = "C:\\Users\\Mateusz\\Desktop\\galeria\\indexed\\"
    files = os.listdir(dest)
    indexes = getDistinctIndexes()
    for index in indexes:
        for file in files:
            fileToDelete = str(index) + ".jpg"
            if file == fileToDelete:
                os.remove(dest+file)


def getDistinctIndexes():
    with open("indexes.txt", "r", encoding="utf-8") as f:
        inputIndexes = f.readlines()
        outputLiczby = []
        for item in inputIndexes:
            liczba = ""
            for n in item:
                if n != " " and n != '\n':
                    liczba = liczba + str(n)
                else:
                    if liczba != " " and liczba != "": outputLiczby.append(liczba)
                    liczba=""
            
        print(inputIndexes)                        
        print(outputLiczby)
        #print(set(inputIndexes))
    
    DistinctIndexes = []    
    for j in outputLiczby:
        if j not in DistinctIndexes:
            DistinctIndexes.append(j)

    return DistinctIndexes

getDistinctIndexes()