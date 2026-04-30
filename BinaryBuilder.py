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
        save_schemz(str(selected_file),schem)
    else:
        print("No runnable files detected! Please put code files inside current dirrectory, with the .mcbi tag.")



def select_file(files):
    while (file_input := input('Select a file:')) not in files:
        print('Not a valid .mcbi file')
    return file_input


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
        return f.readlines()






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
    schem.setBlock((x,y+1,z),"minecraft:structure_void")


def save_schemz(schem_name,schem_file):
    try:
        filen_noextention = schem_name.split('.')[0]
        schem_file.save(".",filen_noextention,mcschematic.Version.JE_1_18_2 )
        print("successfully saved in schem folder!")
    except:
        print("there was an error with saving your schematic")


main()
