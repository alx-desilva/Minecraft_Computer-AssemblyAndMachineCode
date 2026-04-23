import mcschematic
from zmq import error
from asyncio import SelectorEventLoop
from pathlib import Path
from os import listdir
from os.path import isfile, join


"""
posy = -1
for i in range(1,3):
    print(i)
    schem.setBlock((0,posy,0),"minecraft:stone")
    posy -= 3
"""

def main():
    print("checking for runnable files...\n")

    onlyfiles = [f for f in listdir(".") if isfile(join(".", f))]
    mcbifiles = []

    for f in onlyfiles:
        if check_file_type_mcbi(f) == True:
            mcbifiles.append(f)

    if mcbifiles:
        print("Available files:")
        print(mcbifiles)
        selected_file = select_file(mcbifiles)
        schem = make_schemz(selected_file)
        save_schemz("instMemtest",schem)
    else:
        print("No runnable files detected! Please put code files inside current dirrectory, with the .mcbi tag.")




def select_file(files):
    files = files
    file_input = input("Please Select a valid File:")
    for file in files:
        if file_input == file:
            return file
    else:
        main()


def check_file_type_mcbi(file):
    p = Path(file)
    extention = p.suffix.lower()

    if extention == ".mcbi":
        return(True)
    else:
        return(False)

def read_mcbi_file(file):
    converted_binary_list = []
    with open(file,"r") as f:
        for l in f:
            converted_binary_list.append(str(l))
    return converted_binary_list






def make_schemz(schem_file):
    schem = mcschematic.MCSchematic()
    binary_list = read_mcbi_file(schem_file)
    lineNum = 0
    TotalLineNum = 0
    xloc = 0
    zloc = 0
    for binary_line in binary_list:
        if lineNum == 32:
            lineNum = 0
            zloc = 0
            xloc -= 6
        TotalLineNum += 1
        print(f"Current line: {TotalLineNum}")
        create_line(schem,binary_line,xloc,zloc)
        lineNum += 1
        zloc -= 2
    
    return schem


def create_line(schem_file,binary_line,xloc,zloc):
    mid = len(binary_line) // 2
    firstEightBits = binary_line[:mid]
    secondEightBits = binary_line[mid:]

    ydif = -1

    for bit in firstEightBits:
        if bit == "1":
            binary_on(xloc,ydif,zloc, schem_file)
        if bit == "0":
            binary_off(xloc,ydif,zloc, schem_file)
        ydif -= 2
    ydif -=2
    for bit in secondEightBits:
        if bit == "1":
            binary_on(xloc,ydif,zloc, schem_file)
        if bit == "0":
            binary_off(xloc,ydif,zloc,schem_file)
        ydif -= 2

        




def binary_on(x,y,z,schem):
    schem.setBlock((x,y,z),"minecraft:magenta_wool")
    schem.setBlock((x,y+1,z),"minecraft:repeater[facing=east]")


def binary_off(x,y,z,schem):
    schem.setBlock((x,y,z),"minecraft:magenta_wool")


def save_schemz(schem_name,schem_file):
    try:
        schem_file.save(".",schem_name,mcschematic.Version.JE_1_18_2 )
        print("successfully saved in schem folder!")
    except:
        print("there was an error with saving your schematic")


main()
