import os

trash = ["png", "jpg", "mp4", ""]

if __name__ == "__main__":
    desktop = f"{os.path.expanduser('~')}\desktop"
    os.chdir(desktop)
    print(os.getcwd())
    for file in os.listdir():
        print(file)
        file = file.split(".")
        print(file[-1])
        if file[-1] in 
