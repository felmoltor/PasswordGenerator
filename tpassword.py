#!/usr/bin/env python

# Author: Felipe Molina (@felmoltor)
# Date: November 2013
# Summary: This script generate all the posibles strings with a generator or seed file
#            with the characters will be used in the string generation.
#            It is possible to set a template string like "h--" to generate a string 
#            starting allways with 'h'.
# Original Idea: Jonas Andradas (@jandradas)
#
# Example:
#    * eed file Containing letters "a" and "o"
#    * Template like "p-ll-"
#    * Results will be: ['palla', 'pallo', 'polla', 'pollo']

import sys
import os
import argparse
import sqlite3

def printBanner():
    banner = """
     _____  ___                                    _          ___   _ 
    /__   \/ _ \__ _ ___ _____      _____  _ __ __| | __   __/ _ \ / |
      / /\/ /_)/ _` / __/ __\ \ /\ / / _ \| '__/ _` | \ \ / / | | || |
     / / / ___/ (_| \__ \__ \\\\ V  V / (_) | | | (_| |  \ V /| |_| || |
     \/  \/    \__,_|___/___/ \_/\_/ \___/|_|  \__,_|   \_/  \___(_)_|
     
    ****************************************************
    * Password generator with seed chars and templates *
    * Author: @felmoltor                               *
    * Date: November 2013                              *
    * Version: v0.1                                    *
    ****************************************************
    
    """
    print banner

def readUserOptions():
    parser =  argparse.ArgumentParser(description="Password generator with seed chars and templates")
    parser.usage = "%s [OPTIONS] -s <seedfile> -t <template string>" % sys.argv[0]
    parser.add_argument('-t', '--template', help="Template word to fill up with the seed chars",dest="pwdtemplate",default=None,required=True)
    parser.add_argument('-s', '--seed', help="File name with the seed letters",dest="seedfile",default=None,required=True)
    parser.add_argument('-o', '--outputformat', help="TODO: Output format of the generated passwords (sqlite|file|screen). Default is screen.",dest="outformat",default="screen")
    parser.add_argument('-f', '--file', help="Output file name to store results",dest="ofile",default=None)
    args = parser.parse_args()
    
    return args

#########################

def incrementIndexes(idx,base):
    i = len(idx)-1
    while (1):
        idx[i] = (idx[i] + 1) % base
        if idx[i] != 0 or i == 0:
            break
        i -= 1 # Skip to the next index to the left
        
    return idx

#########################

def generatePwdFromIndex(template,seedchars,seedindex):
    templatearr = []
    usedindex = 0
    chposition = 0
    
    # Convertimos a un array de caracteres para modificar de uno en uno
    for ch in template:
        templatearr.append(ch)
    
    for ch in templatearr:
        if (ch == "-"):
            templatearr[chposition] = seedchars[seedindex[usedindex]]
            usedindex += 1
        chposition += 1
    return "".join(templatearr)

#########################

def allZeros(seedindex):
    for idx in seedindex:
        if idx != 0:
            return False
    return True

#########################

def generateFullCombinations(template,seedchars):
    seedindex = []
    nspaces = template.count("-")
    universebase = len(seedchars)
    pwds = []
    
    # Init indexes to create the whole universe from the seed
    n = nspaces
    while (n > 0):
        seedindex.append(0)
        n -= 1 
    
    # Iterate from the [0,0,....,0] array to [n,n,...n]
    pwds.append(generatePwdFromIndex(template,seedchars,seedindex))
    seedindex = incrementIndexes(seedindex,universebase)
    while (not allZeros(seedindex)):
        pwds.append(generatePwdFromIndex(template,seedchars,seedindex))
        seedindex = incrementIndexes(seedindex,universebase)
    
    return pwds

#########################

def calculateUniverseSize(template,seeds):
    nspaces = template.count("-")
    base = len(seeds)
    
    return pow(base,nspaces)

#########################

########
# MAIN #
########

printBanner()
options = readUserOptions()

outputfile = None
seedfile = options.seedfile
pwdtemplate = options.pwdtemplate
if (options.ofile is not None):
    outputfile = options.ofile

if os.path.exists(seedfile):
    sf = open(seedfile,"r")
    seedchars = []
    for line in sf:
        for ch in line.strip():
            if ch not in seedchars: # Avoid repeated chars
                seedchars.append(ch)
    
    seedchars.sort()
    sure = raw_input ("You are going to generate and store %s strings. Are you sure you want to continue? [N/y]: " % calculateUniverseSize(pwdtemplate,seedchars))
    if (sure.upper() == "Y" or sure.upper() == "YES"):
        pwduniverse = generateFullCombinations(pwdtemplate,seedchars)
        # Store in output file if exists
        print "***** DUMPING RESULTS ******"
        if (options.outformat == "file"):
            if (outputfile is not None):
                of = open(outputfile,"w")
                for pwd in pwduniverse:
                    of.write("%s\n" % pwd)
                of.close()
            else:
                for pwd in pwduniverse:
                    print pwd
        elif (options.outformat == "sqlite"):
            if (outputfile is not None):
                if (not (outputfile.endswith(".db"))):
                    outputfile = "%s.db" % outputfile
                oc = sqlite3.connect(outputfile)
                oc.execute('''CREATE TABLE Passwords
                (Password CHAR(%s));''' % len(pwdtemplate))
                for pwd in pwduniverse:
                    oc.execute("INSERT INTO Passwords (Password) VALUES ('%s')")
                oc.close()
            else:
                for pwd in pwduniverse:
                    print pwd
        else:
            for pwd in pwduniverse:
                print pwd
        print "********** DONE ************"
    else:
        print "Operation cancelled by user..."
else:
    print "Error. Seed file %s does not exists." % seedfile