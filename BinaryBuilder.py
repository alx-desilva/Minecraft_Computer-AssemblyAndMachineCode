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
        select_file(files)


def check_file_type_mcbi(file):
    p = Path(file)
    extention = p.suffix.lower()

    if extention == ".mcbi":
        return(True)
    else:
        return(False)


def make_schemz(schem_file):
    schem = mcschematic.MCSchematic()
    binary_list = read_mcbi_file(schem_file)
    yoffset = 0

    for set in binary_list:
        for bit in set:
            if bit == "1":
                binary_on(0,yoffset,0,schem)
            elif bit == "0":
                binary_off(0,yoffset, 0,schem)
            yoffset -= 3
        yoffset = 0

    return schem


def read_mcbi_file(file):
    converted_binary_list = []
    with open(file,"r") as f:
        for l in f:
            converted_binary_list.append(str(l))
    return converted_binary_list





def binary_on(x,y,z,schem):
    schem.setBlock((x,y,z),"minecraft:magenta_wool")
    schem.setBlock((x,y+1,z),"minecraft:repeater")


def binary_off(x,y,z,schem):
    schem.setBlock((x,y,z),"minecraft:magenta_wool")


def save_schemz(schem_name,schem_file):
    try:
        schem_file.save("/Users/alexdesilva/Library/Application Support/minecraft/config/worldedit/schematics",schem_name,mcschematic.Version.JE_1_18_2 )
        print("successfully saved in schem folder!")
    except error:
        print("there was an error with saving your schematic")
        print(error)


main()
