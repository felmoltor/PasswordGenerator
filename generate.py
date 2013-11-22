#!/usr/bin/env python

# Author: Felipe Molina (@felmoltor)
# Date: November 2013
# Summary: This script generate all the posibles strings with a generator or seed file
#            with the characters will be used in the string generation.
#            It is possible to set a template string like "h--" to generate a string 
#            starting allways with 'h'.
# Example:
#    * eed file Containing letters "a" and "o"
#    * Template like "p-ll-"
#    * Results will be: ['palla', 'pallo', 'polla', 'pollo']

import sys
import os

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

########
# MAIN #
########

if (len(sys.argv)!=3):
    print "Usage: %s <seed_file> <template string>" % sys.argv[0]
    print "Example: %s seed.txt Pwd----123" % sys.argv[0]

else:
    seedfile = sys.argv[1]
    pwdtemplate = sys.argv[2]
    
    if os.path.exists(seedfile):
        sf = open(seedfile,"r")
        seedchars = []
        for line in sf:
            for ch in line.strip():
                if ch not in seedchars: # Avoid repeated chars
                    seedchars.append(ch)
        
        seedchars.sort()
        # Get the number of spaces with '-' to fill with the seed chars from pwdtemplate
        pwduniverse = generateFullCombinations(pwdtemplate,seedchars)
        print pwduniverse
    else:
        print "Error. Seed file %s does not exists." % seedfile