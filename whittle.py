#!/usr/bin/env python

#from groupings import groupings
import sys
from re import compile as re_compile, IGNORECASE as re_IGNORECASE, sub as re_sub
import fileinput

def index(req):
    html = """<html>
        <head>
        <title>Hello Word - First CGI Program</title>
        </head>
        <body>"""

    html += "<table>\n"

    count = 1
    for key in sorted(groupings.keys()) :
        html += "<tr><td>\n"
        html += "<td>" + str(count) + "</td>"
        grouping = groupings[key]
        for name in grouping :
            html += "<td>" + name + "</td>\n"
        html += "</tr>\n"
        count += 1

    html += "</table>\n"
    
    html += """</body>
        </html>"""
    return html


def say(req, what="NOTHING"):
    return "I am saying %s" % what

syllables = re_compile(r'[a,e,i,o,y]+', flags=re_IGNORECASE)
blacklist = []
whitelist = {}

fh = open("blacklist.txt", 'r')
while True :
   expr = fh.readline().strip()
   if not expr :
       break
   blacklist.append(re_compile(r'' + expr, flags=re_IGNORECASE))
fh.close()

fh = open("whitelist.txt", 'r')
while True :
   expr = fh.readline().strip()
   if not expr :
       break
   whitelist[expr] = True
fh.close()

def whittle(name) :
    # ignore names with more than two syllables
    if len(syllables.findall(name)) > 2 :
        return False

    # ignore names with double letters
    for char in name :
        if (char + char) in name :
            return False

    # ignore names that are too small
    if len(name) <= 2 :
        return False

    # ignore names with blacklisted regular expression patterns
    for bexpr in blacklist :
        if bexpr.findall(name) :
            return False

    # Ignore names that are copies
    if len(name) > 4 :
        if len(name) % 2 == 0 :
            if name[:len(name)/2] == name[len(name)/2:] :
                return False
    return True

d = {}
#fh = open('dict.txt', 'r')
#while True :
#    word = fh.readline().strip().lower()
#    if not word :
#        break
#    d[word] = True
#fh.close()

prefixes = {}
pnames = {}
names = {}
for kind in sys.argv[1:] :
    fh = open(kind + ".txt", 'r')
    while True :
        name = fh.readline()
        if not name :
            break
        name = name.strip()
        if whittle(name) :
            if name not in d :
                names[name] = True
                for x in range(0, len(name)) :
                    prefix = name[:x] 
                    if prefix not in prefixes :
                        prefixes[prefix] = 0
                        pnames[prefix] = []
                    else :
                        prefixes[prefix] += 1
                    pnames[prefix].append(name)
    fh.close()
    print(str(len(names)) + " names left")

    fh = open(kind + ".txt.out", 'w') 
    for name in names :
        fh.write(name + "\n")
    fh.close()

    while True :
        longest = -1
        lengths = {}
        for prefix_key in prefixes.keys() :
            prefix = prefixes[prefix_key]
            l = len(prefix_key)
            if l not in lengths :
                lengths[l] = {}
            if l > longest and prefix > 1:
                lengths[l][prefix_key] = prefix
                longest = l

        if longest == -1 :
            break

        #print "Longest is: " + str(longest)
        for prefix_key in lengths[longest].keys() :
            if prefix_key in whitelist :
                #print "Already whitelisted: " + prefix_key
                del prefixes[prefix_key] 
                continue

            for name in pnames[prefix_key] :
                print "  " + name
            print "Keep: " + prefix_key + ": " + str(lengths[longest][prefix_key]) + " (y/N) ?"
            # Ask if this prefix is good and if not
            # add it to the blacklist
            for yesno in sys.stdin.readline() :
                if not yesno :
                    break

                if yesno.strip().lower() == "y" :
                    print "Keeping."
                    fh = open("whitelist.txt", 'a')
                    fh.write(prefix_key + "\n")
                    fh.close()
                    break

                print "Blacklisting."
                fh = open("blacklist.txt", 'a')
                fh.write("^" + prefix_key + "\n")
                fh.close()

            del prefixes[prefix_key] 
