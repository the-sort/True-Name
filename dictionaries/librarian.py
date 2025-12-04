"""
Procesing downloaded words.txt files
"""
from argparse import ArgumentParser
from os       import remove

parser = ArgumentParser(description = "Process file to game resource")

parser.add_argument("file", help = "file for process")
parser.add_argument(    "-d", "-D", "--delete",
                        default = False ,
                        action  = "store_true",
                        help    = "delete file after procesing"
                    )
args = parser.parse_args()
new_file_name = str(args.file).removesuffix(".txt") + "_edited.txt"


try:
    with open(args.file, mode = "rt", encoding= "utf-8") as file:
        with open(new_file_name, mode ="wt+", encoding="utf-8") as new_file:
            for line in file:
                separeted = line.split("\t")
                if  (   len(separeted[0]) <= 2      or
                        not separeted[0].isalpha()  or
                        len(separeted[0]) > 15
                    ):
                    continue
                if int(separeted[1]) < 15:
                    break
                new_file.write((separeted[0]+"\n").upper())
        if args.delete:
            remove(args.file)
            print("File: ", args.file, " was deleted")

except FileNotFoundError:
    print("File does not exist in this Folder")
except PermissionError:
    print("Inssuficient permisions")
