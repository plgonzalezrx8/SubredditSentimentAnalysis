
import glob

counter = 0
cache = []


# Get rid of empty lines
def cleanemptylines(filename):
    print("Now cleaning the text file for whitespaces")
    print("Current file is %s " % (filename))
    # Get file contents
    fd = open(filename, encoding="utf8")
    contents = fd.readlines()
    fd.close()

    new_contents = []

    for line in contents:
        # Strip whitespace, should leave nothing if empty line was just "\n"
        if not line.strip():
            continue
    # We got something, save it
        else:
            new_contents.append(line)

# make new file without empty lines

    fd = open(filename, "w", encoding="utf8")

    fd.write("".join(new_contents))
    print("successfully done")
    fd.close()

    print("Cleaning Complete")

# this line will gather all the txt files in the directory, might need some tweaking to work in your environment.


txt_file_list = glob.glob("parsed_comments/*.txt")

# this will clean all the txt files in the current directory.
# By cleaning I mean removing all the spaces and unsupported symbols.


for i in txt_file_list:
    cleanemptylines(i)


