from asyncio import SelectorEventLoop
from pathlib import Path
from os import listdir
from os.path import isfile, join

Version = 0.1

commands = {
    "NOP": "0000",
    "LDR":"0001",
    "ADD": "0010",
    "SUB": "0011",
    "AND": "0100",
    "OR": "0101",
    "NAND": "0110",
    "XOR": "0111",
    "HLT": "1000",
    "JMP": "1001",
    "": "1010",
    "LOD": "1011",
    "STR": "1100",
    "": "1101",
    "": "1110",
    "": "1111",
    "R0": "0000",
    "R1": "0001",
    "R2": "0010",
    "R3": "0011",
    "R4": "0100",
    "R5": "0101",
    "R6": "0110",
    "R7": "0111",
    "R8": "1000",
    "R9": "1001",
    "R10": "1010",
    "R11": "1011",
    "R12": "1100",
    "R13": "1101",
    "R14": "1110",
    "R15": "1111"
}

print(commands["AND"])

def startup():
    print(f"Welcome to Coco's V{Version} Machine Code interpreter. \n This is built for a minecraft computer project. All commands and info are on Github! \n")
    main()

def main():
    print("checking for runnable files...\n")

    onlyfiles = [f for f in listdir(".") if isfile(join(".", f))]
    mcmcfiles = []
    
    for f in onlyfiles:
        if check_file_type_mcmc(f) == True:
            mcmcfiles.append(f)
    
    if mcmcfiles:
        print("Available files:")
        print(mcmcfiles)
        Selected_file = select_file(files=mcmcfiles)
        binary = convert_script(str(Selected_file))
        export_to_file(binary,Selected_file)
    else:
        print("No runnable files detected! Please put code files inside current dirrectory, with the .mcmc tag.")

    


def select_file(files):
    files = files
    file_input = input("Please Select a valid File:")
    for file in files:
        if file_input == file:
            return(file)
    else:
        select_file(files)


def convert_script(file):
    with open(file) as f:
        binary_line_list = []
        for line in f:
            cur_line_binary = ""
            line_code_list = line.split()
            print(line_code_list)
            for code in line_code_list:
                print(code)
                for key, value in commands.items():
                    if code == key:
                        cur_line_binary += str(value)
            binary_line_list.append(cur_line_binary)
        f.close()
    
    return(binary_line_list)



def check_file_type_mcmc(file):
    p = Path(file)
    extention = p.suffix.lower()

    if extention == ".mcmc":
        return(True)
    else:
        return(False)

def export_to_file(binary_list,file_name):
    filen_noextention = file_name.split('.')[0]
    try:
        with open(filen_noextention+ ".mcbi","w") as f:
            for line in binary_list:
                f.write(str(line)+ "\n")
            f.close()
            print(f"Successfully exported binary to: {filen_noextention}.mcbi")

    except:
        print("There was a probelm exporting your script!")
    main()
    

startup()