import json
import glob
import os


name = raw_input("\nEnter your name: ")

# list of all json files i.e. all blocks
files = [f for f in glob.glob("*.json")]

index = 0
for f in files:

    # get block number, index of char in file name
    i = f[6]

    # open the json file
    file_name = "block_" + i + ".json"
    fopen = open(file_name,)
    data = json.load(fopen)

    for trans in data["transactions"]:

        if (name in trans):
            print("Match!")
            print("amount: " + str(trans[2]))
            
