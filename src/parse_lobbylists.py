#!/usr/bin/python

import re

def is_phone_number(line):
    # a phone number does not contain any letters, does not contain '#', and contains 3 numbers in a row
    numbersonly = re.search(r'^[\d\W]+$', line)
    return numbersonly

def should_skip_line(line):
    # skip the 3 filler lines at the start of each page of the pdf
    if ('Professional Lobbyist Directory' in line or
        line.startswith('Lobbyist Principal...') or 
        line.startswith('Page ')):
#        print 'Skipping', line
        return True
    if is_phone_number(line):
#        print 'Skipping phone number ', line
        return True
    if re.search(r'^\s+$', line):
#        print 'Skipping whitespace ', line
        return True
#    print line
    return False

def parse_corporation(line, f, lobbyist_id):
    # first line is name, then address
    name = line
    address = parse_address(f)
    return ['corporation', lobbyist_id, name, address]

def is_new_lobbyist_start(line):
    match = re.search(r'\sProfessional\s+\d+', line)
    return match

def parse_lobbyist(line, f):
    # First line is <Lobbyist name/title> - Professional - <id number>
    match = re.search(r'^(.+)\s+Professional\s+(\d+)', line)
    if match:
        name = match.group(1)
        id = match.group(2)
    else:
        print 'ERROR parsing lobbyist name for line', line
    # next lines are addresses
    address = parse_address(f)
    return ['lobbylist', id, name, address]
    
def finished_parsing_address(line):
    # End of address is signified by <city> CO <5-digit zip>
    match = re.search(r'[\s\w]+\s\w\w\s\d{5,6}$', line, re.IGNORECASE)
    return match

def parse_address(f):
    found_address = False
    address = ""
    count = 1
    while (not found_address):
        line = f.readline()
        if not line:
            break
        line = line.strip()
        if should_skip_line(line):
            continue
        count +=1
        address += line
        found_address = finished_parsing_address(line)
        if (not found_address):
            address += ','
    return address

fname = "../data/lobbyists_clean.txt";
#fname = "../data/test_new2.txt";

current_lobbyist = ""
current_corporation = ""
with open(fname) as f:
    line = f.readline()
    while(line):
        line = line.strip()
        if should_skip_line(line):
            line = f.readline()
            continue
        # starting a new lobbyis`t
        if is_new_lobbyist_start(line):
            current_lobbyist = parse_lobbyist(line, f)
            print '|'.join(current_lobbyist)
        # start a new corporation corresponding to current lobbyist
        else:
            current_corporation = parse_corporation(line, f, current_lobbyist[1])
            print '|'.join(current_corporation)
        line = f.readline()



