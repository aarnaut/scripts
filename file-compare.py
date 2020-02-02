import argparse
import os
import sys
import hashlib

def calculateChecksum(fileName):
    hash = hashlib.md5()
    with open(fileName, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()

parser = argparse.ArgumentParser()
parser.add_argument('filesToCompare', help='files to compare', metavar='FILE', nargs='+')

args = parser.parse_args()
checksums = []

for path in args.filesToCompare:
    if os.path.isfile(path):
        checksum = calculateChecksum(path)
        checksums.append(checksum)
        print("file: '%s' MD5: '%s'" % (path, checksum))
    else:
        print("path '%s' is not a file" % (path))
        sys.exit()

if len(set(checksums)) == 1:
  print("files match")
else:
  print("files don't match")
