""" Made by AmazingChz - https://github.com/AmazingChz/ """

#########################################
#Parse *.pchtxt files (used by IPSwitch)#
#########################################

"""

HOW TO USE:
-----------

"parserIPS.py <*.pchtxt_file_dir>"

"""

import sys
import io
import time

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def parser():
    
    file = str(sys.argv[1])
    
    ###########################################################################

    # Getting names...

    pchtxt = open(file, "r")

    names = []
    for lines in pchtxt:
        pchtxt = open(file, "r")
            
        lines = str(lines)
        try:
            if lines.startswith("// "):
                names.append(lines)
        except:
            pass
        
    pchtxt.close()

    ###########################################################################

    # Getting settings...

    pchtxt = open(file, "r")

    settings = []
    for lines in pchtxt:
        pchtxt = open(file, "r")
            
        lines = str(lines)
        try:
            if lines.startswith("@enabled") or lines.startswith("@disabled"):
                settings.append(lines)
        except:
            pass
        
    pchtxt.close()
    
    ###########################################################################
    
    # Getting offsets and patches...

    offsets = []
    patches = []

    pchtxt = open(file, "r")
    for lines in pchtxt:
        pchtxt = open(file, "r")
            
        try:
            lines = str(lines)

            #Checking if there is a new patch being added (overall)...
            check = lines[1:2]
            if check == "":
                pass
            else:
                offsets.append("\n")
                patches.append("\n")
                
            tokens = lines.split(" ")

            #Adding patches from each line...
            pat = []
            try:
                if int(tokens[0], 16):
                    for i in range(len(tokens)):
                        if i != 0:
                            pat.append(tokens[i])

                    #Adding space between text in lines, when necesarry...
                    p = ""
                    for i in range(len(pat)):
                        checker = pat[i].startswith(" ")
                        if i != 0 and checker == False:
                            p += " "
                            
                        p += pat[i]

                    try:
                        p = p.replace("\n", "")
                    except:
                        pass

                    offsets.append(str(tokens[0]))
                    patches.append(p)
            except:
                pass
        except:
            continue
        
    pchtxt.close()

    ###########################################################################

    # Writing data to files...

    n = open(resource_path(".\\resources\\tools\\parserIPS\\resources\\names.txt"), "w")
    for items in names:
        n.write(items)
    n.close()

    #---

    s = open(resource_path(".\\resources\\tools\\parserIPS\\resources\\settings.txt"), "w")
    for items in settings:
        s.write(items)
    s.close()

    #---

    o = open(resource_path(".\\resources\\tools\\parserIPS\\resources\\offsets.txt"), "w")
    for items in offsets:
        o.write(items)
    o.close()

    #---

    p = open(resource_path(".\\resources\\tools\\parserIPS\\resources\\patches.txt"), "w")
    for items in patches:
        p.write(items)
    p.close()

    #---

    #print('\n\nYour *.pchtxt data has been successfully saved into the "resources" folder.\n')

if __name__ == "__main__":
    if len(sys.argv) == 2:
        parser()
    elif len(sys.argv) < 2:
        print('\n\nNot enough args.\n\nUsage: "parserIPS.py <*.pchtxt_file_dir>"\n')
    else:
        print('\n\nToo many args.\n\nUsage: "parserIPS.py <*.pchtxt_file_dir>"\n')
