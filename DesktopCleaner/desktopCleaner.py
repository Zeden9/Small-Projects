import os
import shutil
from datetime import date as d
import gui 

trash = ["h","cpp","prg", "rzk","msi","zip", "7zip", "rar","png", "jpg", "mp4", "pdf", "gif", "ico", "bat", "txt", "srt", "mp3", "doc", "docs", "docx", "avi", "exe", "py"]

if __name__ == "__main__":
    #desktop = f"{os.path.expanduser('~')}\desktop" #Setting directory to current user's desktop
    #destination = f"{desktop}\{d.today()}"

    desktop = f"{os.path.expanduser('~')}\\desktop"     #Setting directory to current user's desktop
    if not os.path.exists(f"{desktop}\\desktops"):      #checking if working folder already exists
        os.mkdir(f"{desktop}\\desktops")

    destination = f"{desktop}\\desktops\\{d.today()}"    #Setting destination directory 
    if not os.path.exists(destination):     #checking if destination already exists
        os.mkdir(destination)

    os.chdir(desktop)   #Changing directory 
    
    for file in os.listdir():     #Looping through all files and directories on desktop 
        if file == "desktops": continue
        fileSplit = file.split(".")    #Distinguishing the type
        print(fileSplit[-1])    
        
        if os.path.isdir(file):   #Checking if files is a directory
            print(f"{file} is a directory")
            notAnswered = True
            while notAnswered:
                answer = input("Do you want to move that directory? Y/N")
                if answer.lower() == "y":
                    shutil.move(file, f"{destination}\{file}")
                    
                    notAnswered = False
                elif answer.lower() == "n":
                    notAnswered = False
                else: print("Wrong data")
        else:
            if fileSplit[-1] in trash:       #checking if file is a trash type
                curDestination = f"{destination}\{fileSplit[-1]}"
                if not os.path.exists(curDestination): os.mkdir(curDestination)
                shutil.move(file, curDestination)
                
