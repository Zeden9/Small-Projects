import os
import shutil
from datetime import date as d
import json
import gui 

def load_trash_config(config_path):
    """Load trash extensions from config file, or create default if not exists."""
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
            return set(config.get("trash_extensions", []))
    else:
        # Default trash extensions
        default_trash = {"h", "cpp", "prg", "rzk", "msi", "zip", "7zip", "rar", 
                        "png", "jpg", "mp4", "pdf", "gif", "ico", "bat", "txt", 
                        "srt", "mp3", "doc", "docs", "docx", "avi", "exe", "py"}
        save_trash_config(config_path, default_trash)
        return default_trash

def save_trash_config(config_path, trash_set):
    """Save trash extensions to config file."""
    config = {"trash_extensions": sorted(list(trash_set))}
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

def ask_about_extension(extension):
    """Ask user if an unknown extension should be treated as trash."""
    while True:
        answer = input(f"Unknown extension '.{extension}' found. Move to trash? (Y/N): ").lower()
        if answer in ["y", "n"]:
            return answer == "y"
        print("Invalid input. Please enter Y or N.")

if __name__ == "__main__":
    desktop = f"{os.path.expanduser('~')}\\desktop"     #Setting directory to current user's desktop
    config_path = f"{desktop}\\desktops\\trash_config.json"
    
    if not os.path.exists(f"{desktop}\\desktops"):      #checking if working folder already exists
        os.mkdir(f"{desktop}\\desktops")

    # Load trash configuration
    trash = load_trash_config(config_path)
    
    destination = f"{desktop}\\desktops\\{d.today()}"    #Setting destination directory 
    if not os.path.exists(destination):     #checking if destination already exists
        os.mkdir(destination)

    os.chdir(desktop)   #Changing directory 
    
    for file in os.listdir():     #Looping through all files and directories on desktop 
        if file == "desktops": continue
        fileSplit = file.split(".")    #Distinguishing the type
        extension = fileSplit[-1]
        print(extension)    
        
        if os.path.isdir(file):   #Checking if files is a directory
            print(f"{file} is a directory")
            notAnswered = True
            while notAnswered:
                answer = input("Do you want to move that directory? Y/N: ").lower()
                if answer == "y":
                    shutil.move(file, f"{destination}\\{file}")
                    notAnswered = False
                elif answer == "n":
                    notAnswered = False
                else: 
                    print("Wrong data")
        else:
            # Check if extension is in trash, or ask user if unknown
            if extension not in trash:
                if ask_about_extension(extension):
                    trash.add(extension)
                    save_trash_config(config_path, trash)
                else:
                    continue
            
            # Move file to appropriate trash folder
            curDestination = f"{destination}\\{extension}"
            if not os.path.exists(curDestination): 
                os.mkdir(curDestination)
            shutil.move(file, curDestination)
                
