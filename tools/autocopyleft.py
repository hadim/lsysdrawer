#-*- coding: utf-8 -*-

import sys, fileinput, os

# Configuration
path_src = "../src/"
fextension = [".py"]
date_copyright = "2011"
authors = "see AUTHORS"
project_name = "ProfileExtractor"
header_file = "license_header.txt"

def pre_append(line, file_name):
    fobj = fileinput.FileInput(file_name, inplace=1)
    first_line = fobj.readline()
    sys.stdout.write("%s\n%s" % (line, first_line))
    for line in fobj:
        sys.stdout.write("%s" % line)
    fobj.close()

def listdirectory(path, extension): 
    all_files = [] 
    for root, dirs, files in os.walk(path): 
        for i in files:
            if os.path.splitext(i)[1] in extension:
                all_files.append(os.path.join(root, i)) 
    return all_files

if __name__ == '__main__':

    f = open(header_file, 'r')
    licence_head = f.readlines()
    f.close()

    files = listdirectory(path_src, fextension)

    for f in files:

        name = os.path.basename(f)
        str_lhead = ""
        for l in licence_head:
            l = l.replace("DATE", date_copyright)
            l = l.replace("AUTHORS", authors)
            l = l.replace("PROJECT_NAME", project_name)
            l = l.replace("FILENAME", name)
            str_lhead += l
    
        pre_append(str_lhead, f)
    
