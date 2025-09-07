import shutil
import os
import keyboard
import sys
import json
import tkinter as tk
from tkinter import filedialog
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
root = tk.Tk()
root.withdraw()
root.attributes('-topmost', True)

dirNames = {}
if os.path.isfile("C:/Users/ronni/AppData/Local/Programs/fileSorter/sortData.dat"):
    with open("C:/Users/ronni/AppData/Local/Programs/fileSorter/sortData.dat") as f:
        dirNames = json.loads(f.read())
else:
    os.makedirs("C:/Users/ronni/AppData/Local/Programs/fileSorter/sortData.dat")


def dirSort(dirName):
    global index
    index = 0
    dirNameContents = dirNames.get(dirName)
    if dirNameContents is None:
        print(f"Directory '{dirName}' not found in configuration.")
        return
    categories = dirNameContents.get("categories")
    workDir = dirNameContents.get("dir")
    dirContents = os.listdir(workDir)
    categories = dirNameContents.get("categories")
    workDir = dirNameContents.get("dir")
    dirContents = os.listdir(workDir)
    for file in dirContents:
        file_path = os.path.join(workDir, file)
        try:
            dest_folder = categories.get(os.path.splitext(file)[1])
            if dest_folder is not None:
                shutil.move(file_path, os.path.join(workDir, dest_folder))
            else:
                raise KeyError("No category for this extension")
        except Exception:
            if not os.path.isfile(file_path):
                folder_dest = categories.get('folders')
                misc_dest = categories.get('misc')
                if folder_dest is not None:
                    try:
                        shutil.move(file_path, os.path.join(
                            workDir, folder_dest))
                    except Exception:
                        if misc_dest is not None:
                            shutil.move(file_path, os.path.join(
                                workDir, misc_dest))
                elif misc_dest is not None:
                    shutil.move(file_path, os.path.join(workDir, misc_dest))
            else:
                misc_dest = categories.get('misc')
                if misc_dest is not None:
                    shutil.move(file_path, os.path.join(workDir, misc_dest))


def selector(options: list, *title):
    selecting = True

    def printTitle():
        global index
        os.system("cls")
        for i in title:
            print(i)
        for i in options:
            if options.index(i) == index:
                print(f"\033[1m>\033[0m{i}")
            else:
                print(i)
    printTitle()

    def onDown(e):
        global index
        if index < len(options)-1:
            index += 1
            printTitle()
        return

    def onUp(e):
        global index
        if index > 0:
            index -= 1
            printTitle()
        return

    def onEnter(e):
        nonlocal selecting
        selecting = False
    keyboard.on_press_key("down", onDown)
    keyboard.on_press_key("up", onUp)
    keyboard.on_press_key("right", onEnter)
    while selecting:
        ()
    keyboard.unhook_all()
    os.system("cls")
    return index


def editDir(dirName):
    dirToEdit = dirNames.get(dirName)
    while True:
        match selector(["\x1b[32mAdd Subcategory\x1b[0m",
                       "\x1b[34mEdit Dir\x1b[0m", "\x1b[31mDelete Subcategory\x1b[0m\n", "Save Changes"], f"Your are editing the \033[1m\x1b[32m{dirName}\x1b[0m\033[0m Director", "How would you like to edit this directory?", "="*36):
            case 0:
                subcategoryDir = filedialog.askdirectory(
                    initialdir=dirToEdit["dir"])
                match selector(["By extension", "If folder"], "How Should this subcategory be sorted?", "="*36):
                    case 0:
                        print("Type the extension")
                        extension = input("including the dot -> ")
                        dirToEdit["categories"][extension] = os.path.relpath(
                            subcategoryDir, dirToEdit["dir"])
                    case 1:
                        dirToEdit["categories"]["folder"] = os.path.relpath(
                            subcategoryDir, dirToEdit["dir"])

            case 1:
                dirNames[dirName]["dir"] = filedialog.askdirectory()
            case 2:
                categoryItems = list(dirNames[dirName]["categories"].items())
                categoryKeys = list(dirNames[dirName]["categories"].keys())
                categorySelector = []
                for i in range(len(categoryKeys)):
                    categorySelector.append(
                        f"{categoryItems[i]} | {categoryKeys[i]}")
                dirNames[dirName]["categories"].pop(categoryKeys[
                                                    selector(categorySelector, "Choose Subcategory to delete", "="*36)])
            case 3:
                with open("C:/Users/ronni/AppData/Local/Programs/fileSorter/sortData.dat", "w") as f:
                    json.dump(dirNames, f)


sysArgs = sys.argv
selecting = True
index = 0
if sysArgs[0] in dirNames:
    dirSort(dirNames.get(sysArgs[0]))
else:
    match selector(["Sort Files", "Add or edit dir"], "My Website - \x1B[4m\x1B[34mhttps://flatcapdesign.co.uk/ronnie/\x1B[0m", "Welcome to fileSorter.py                   \x1B[30mVer 1.0\x1B[0m", "This helps with sorting files into various folders", "="*36):
        case 0:
            sortIndex = selector(
                ["\x1b[32mSort All\x1b[0m"] + list(dirNames.keys()), "Select directory to sort", "Sort All will sort all of the listed directories", "="*36)
            if sortIndex == 0:
                for i in list(dirNames.keys()):
                    dirSort(i)
            else:
                dirSort(list(dirNames.keys())[sortIndex-1])
        case 1:
            dirAndName = ["\x1b[32mAdd Dir\x1b[0m"]
            for i in list(dirNames.keys()):
                dirAndName.append(
                    f"{i} | \x1b[34m{dirNames.get(i).get('dir')}\x1b[0m")
            dirAndName.append("\x1b[31mDelete Dir\x1b[0m")

            dirIndex = selector(
                dirAndName, "Add dir or select one to edit", "="*36)
            if dirIndex == 0:
                currDir = filedialog.askdirectory()
                if currDir == "":
                    sys.exit()
                currDirName = ""
                while True:
                    currDirName = input(
                        "What would you like to call this directory? -> ").lower()
                    if currDirName in list(dirNames.keys()):
                        print("==========")
                        print("That name is already used")
                        print("==========")
                    elif currDirName == "":
                        print("==========")
                        print("You have to have a name")
                        print("==========")
                    else:
                        break
                dirNames[currDirName] = {"dir": currDir, "categories": {}}
                editDir(currDirName)
            elif dirIndex == len(list(dirNames.keys()))+1:
                tempDirAndName = dirAndName.copy()
                tempDirAndName.pop(0)
                tempDirAndName.pop()
                dirNames.pop(
                    list(dirNames.keys())[selector(tempDirAndName, "Which dir would you like to delete", "="*36)])
                with open("C:/Users/ronni/AppData/Local/Programs/fileSorter/sortData.dat", "w") as f:
                    json.dump(dirNames, f)
            else:
                editDir(list(dirNames.keys())[dirIndex-1])
