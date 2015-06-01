#!/usr/bin/python
# -*- coding: UTF8 -*-

import sys
import codecs
import re
import glob, os
import math

phones = ["AH", "r", "g", "y", "u0", "i1",
"b", "z", "f", "v", "i0", "uu1",
"t", "s", "q", "p", "AA", "ii1",
"SH", "k", "G", "UU0", "U1",
"j", "S", "l",  "d", "J", "II0", "I1",
"H", "D", "m", "aa", "A", "UU1",
"x", "T", "n", "uu0", "U0", "II1",
"d", "Z", "h", "ii0", "I0", "sil", 
"TH", "E", "w", "a", "u1", "sp", "^"]

consonants = ["AH", "r", "g", "y",
"b", "z", "f", "v",
"t", "s", "q", "p",
"SH", "k", "G", "J",
"j", "S", "l", "d",
"H", "D", "m",
"x", "T", "n",
"d", "Z", "h", 
"TH", "E", "w", "^"]

vowels = ["aa", "A", "UU1", "II1",
"uu0", "U0", "II0", "I1",
"ii0", "I0",  "UU0", "U1",
"a", "u1", "AA", "ii1",
"i0", "uu1", "u0", "i1"]

stops = ["AH", "b", "t", "T", "b", "p", "d", "D", "k" , "q", "J", "G"]
fricVoiced = ["v", "TH", "z", "Z", "j", "g", "E"]
fricVoiceless = ["f", "S", "s", "^", "SH", "x", "H", "h"]
nasals = ["m", "n"]
trill = ["r"]
approx = ["w", "y", "l"]

pause = ["sil", "sp"]

types = {"phones": phones, "consonants" : consonants, "vowels": vowels, "stops": stops, "fricVoiced": fricVoiced, "fricVoiceless": fricVoiceless, "nasals": nasals, "trill": trill, "approx": approx, "pause": pause}

orgDir = sys.argv[1] #Directory if original segmentations (either manually or automatically)
corDir = sys.argv[2] #Directory of manually corrected segmentations

org = {} #Original boundary data stored in a dictionary where each key is the filename from which the data was taken
cor = {} #Corrected boundary data stored in a dictionary where each key is the filename from which the data was taken
histos = {} #Histograms for each boundary type and the collective (all-data) histogram
deltas = {} #The average delta for each boundary and the collective data

for type1 in types: #Initialise histograms and deltas to zero
	for type2 in types:
		histos[type1 + "-" + type2] = [0, 0, 0, 0, 0, 0, 0 ,0 ,0, 0, 0] #[within 0.005 seconds, 0.01, 0.015, 0.02,.....................
		deltas[type1 + "-" + type2] = [0, 0, 0, 0, 0] #[sum of deltas of boundaries of each type, number of boundaries of that type, # of positive deltas, # of negative deltas, STD]

for file in glob.glob(os.path.join(orgDir, '*.TextGrid')): #Read Original boundaries
	fileHandle = open(file, 'r');
	
	fileName = os.path.split(file)[1]
	fileName = re.sub('_', ' ', fileName)
	fileName = re.sub('  ', ' ', fileName)
	org[fileName] = []
	
	xmax = None
	for line in fileHandle:
		line = re.sub(' ', '', line)
		line = re.sub('\t', '', line)
		line = re.sub('\n', '', line)
		line = re.sub('\r', '', line)
		line = re.sub('"', '', line)
		line = re.sub('\'', '', line)
		line = line.split('=')
		if(len(line) == 2 and line[0] == 'xmax'):
			xmax = float(line[1])
		if(len(line) == 2 and line[0] == 'text' and line[1] in phones and xmax != None):
			org[fileName].append((line[1].strip('"\''), xmax))
			xmax = None
	fileHandle.close()

for file in glob.glob(os.path.join(corDir, '*.TextGrid')): #Read corrected boundaries
	fileHandle = open(file, 'r');
	
	fileName = os.path.split(file)[1]
	fileName = re.sub('_', ' ', fileName)
	fileName = re.sub('  ', ' ', fileName)
	cor[fileName] = []
	
	xmax = None
	for line in fileHandle:
		line = re.sub(' ', '', line)
		line = re.sub('\t', '', line)
		line = re.sub('\n', '', line)
		line = re.sub('\r', '', line)
		line = re.sub('"', '', line)
		line = re.sub('\'', '', line)
		line = line.split('=')
		if(len(line) == 2 and line[0] == 'xmax'):
			xmax = float(line[1])
		if(len(line) == 2 and line[0] == 'text' and line[1] in phones and xmax != None):
			cor[fileName].append((line[1].strip('"\''), xmax))
			xmax = None
	fileHandle.close()

#--------------------------------------------------------------------------------------------------------------------------
#Calculate stats-----------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
	
for fileName in cor: #Start calculating histograms
	if(fileName in org):
		orgUtt = org[fileName]
		corUtt = cor[fileName]
		orgPos = 0
		corPos = 0
		while orgPos < len(orgUtt) - 1 and corPos < len(corUtt) - 1:
			delta = orgUtt[orgPos][1] - corUtt[corPos][1]
			if(math.fabs(delta) < 0.06):
				if(orgUtt[orgPos][0] == corUtt[corPos][0] and orgUtt[orgPos + 1][0] == corUtt[corPos + 1][0]):
					for type1 in types: #For all boundary types, add the delta to the statistics
						for type2 in types: #---------------------------------------------------
							if(orgUtt[orgPos][0] in types[type1] and orgUtt[orgPos + 1][0] in types[type2]): #--
								deltas[type1 + "-" + type2][0] += delta
								deltas[type1 + "-" + type2][1] += 1
								if(delta > 0):
									deltas[type1 + "-" + type2][2] += 1
								if(delta < 0):
									deltas[type1 + "-" + type2][3] += 1
								deltas[type1 + "-" + type2][4] += delta * delta
								
								index = int(math.fabs(delta) / 0.005) #The delta divided by .005 determines the boundary accuracy
								if(index < len(histos[type1 + "-" + type2])):
									histos[type1 + "-" + type2][index] += 1
								else: #All boundaries greater than a certain threshold are added to the last entry of the histogram. This is determined by the length of the list (see if statement above)
									histos[type1 + "-" + type2][-1] += 1
				orgPos += 1
				corPos += 1
			elif delta < -0.06: #If correction is too big then attempt to increase the original or correct boundaries lists pointers to restart comparing
				orgPos += 1
			else:
				corPos += 1

for key in histos:
	print key
	print histos[key]
	if(deltas[key][1] != 0):
		deltas[key][0] = float(deltas[key][0]) / float(deltas[key][1])
		deltas[key][4] = (float(deltas[key][4]) / float(deltas[key][1])) - (deltas[key][0] * deltas[key][0])
	print deltas[key]
	