import argparse
import os
import sys
import re
import glob

# reads the trema file line by line
# extracts the key name, that is the part between the quotes in <text key="">
# builds a list of all the keys and returns the list
def parseTremaFile(fileName):
    print("extracting keys from the trema file...")
    localizationKeyRegex = re.compile('<text key="?.*">')
    localizationKeys = []

    with open(fileName, encoding="utf-8") as file:
        for line in file:
            localizationKeyMatch = re.search(localizationKeyRegex, line)
            if localizationKeyMatch:
                localizationKeyLine = line[localizationKeyMatch.start():localizationKeyMatch.end()] # extract the string
                localizationKeyStart = localizationKeyLine.find('"')
                localizationkeyEnd = localizationKeyLine.find('"', localizationKeyStart + 1, len(localizationKeyLine))
                localizationKeys.append(localizationKeyLine[localizationKeyStart + 1:localizationkeyEnd]) # take only what is between the quotes
    
    return localizationKeys

# reads all the source files and looks for dead localization keys
# if a key is found once, it will not be searched for again
# once there are no keys left or there are no files to read, the method will finish
# it returns the result of the lookup, which is dead localization keys
def lookForDeadKeys(rootFolder, localizationKeys):
    print("looking for dead keys...")
    deadLocalizationKeys = localizationKeys

    for filename in glob.iglob(rootFolder + '**/*.java', recursive=True):
        if len(deadLocalizationKeys) == 0:
            print("done")
            return deadLocalizationKeys

        with open(filename, encoding="utf-8") as file:
            for line in file:
                foundKey = "NONE"
                for key in deadLocalizationKeys:
                    if (line.find(key) != -1):
                        foundKey = key
                        print("found key %s" % (key))
                        break

                if foundKey in deadLocalizationKeys:
                    deadLocalizationKeys.remove(foundKey)
                    print("size %s" % (len(deadLocalizationKeys)))

parser = argparse.ArgumentParser()
parser.add_argument('trema', help='trema file to purge', metavar='FILE')
parser.add_argument('rootFolder', help='root folder to analyze recursively', metavar='FILE')

args = parser.parse_args()
localizationKeys = parseTremaFile(args.trema)
deadLocalizationKeys = lookForDeadKeys(args.rootFolder, localizationKeys)

for key in deadLocalizationKeys:
    print(key)