#!/usr/bin/python
# -*- coding: UTF8 -*-

import sys
import codecs
import re
import glob, os
import math

consonants = ["AH", "r", "g", "y", "Ah",
"b", "z", "f", "v",
"t", "s", "q", "p",
"SH", "k", "G", "J",
"j", "S", "l", "d",
"H", "D", "m",
"x", "T", "n",
"d", "Z", "h", 
"TH", "E", "w", "^",
"AHAH", "rr", "gg", "yy", "AhAh",
"bb", "zz", "ff", "vv",
"tt", "ss", "qq", "pp",
"SHSH", "kk", "GG",
"jj", "SS", "ll",  "dd", "JJ",
"HH", "DD", "mm",
"xx", "TT", "nn",
"dd", "ZZ", "hh", 
"THTH", "EE", "ww", "^^"
]
vowels = ["aa", "A", "UU1", "II1",
"uu0", "U0", "II0", "I1",
"ii0", "I0",  "UU0", "U1",
"a", "u1", "AA", "ii1",
"i0", "uu1", "u0", "i1"
]
pause = ["sil", "sp"
]
phones = consonants + vowels#+ ["", "-", "DIST", "Dist", "dist"]
allSymbols = phones + pause
stopsVoiced = ["b", "d", "D", "G", "J",
"bb", "dd", "DD", "GG", "JJ"
]
stopsVoiceless = ["p", "t", "T", "AH", "k", "q", "Ah",
"pp", "tt", "TT", "AHAH", "kk", "qq", "AhAh"
]
stops = stopsVoiced + stopsVoiceless
fricVoiced = ["v", "TH", "z", "Z", "j", "g", "E",
"vv", "THTH", "zz", "ZZ", "jj", "gg", "EE"
]
fricVoiceless = ["f", "S", "s", "^", "SH", "x", "H", "h",
"ff", "SS", "ss", "^^", "SHSH", "xx", "HH", "hh"
]
fric = fricVoiced + fricVoiceless
nasals = ["m", "n",
"mm", "nn"
]
trill = ["r",
"rr"
]
approx = ["w", "y", "l",
"ww", "yy", "ll"
]

types = {"phones": phones, "consonants" : consonants, "vowels": vowels, "stops": stops, "stopsVoiced": stopsVoiced, "stopsVoiceless": stopsVoiceless, "fric": fric, "fricVoiced": fricVoiced, "fricVoiceless": fricVoiceless, "nasals": nasals, "trill": trill, "approx": approx, "pause": pause}

dir = sys.argv[1] #Text Grids are here
prevType = ""
curType = ""
subs = 0

for file in glob.glob(os.path.join(dir, '*.TextGrid')): #Read Original boundaries
	fileHandle = open(file, 'r');
	
	lines = fileHandle.readlines()
	res = "";
	
	toReplace = []
	labels = ""
	for i in range(0, len(lines)):
		res += lines[i]
		#once at an InterbalTier called phones
		if lines[i].strip() == "class = \"IntervalTier\"" and i < len(lines) - 1 and lines[i + 1].strip() == "name = \"phones\"":
			inIntervals = False
			for j in range(i + 1, len(lines)):
				res += lines[j]
				if(lines[j].strip().split(' ')[0].strip() == "item"):
					inIntervals = False
				if(lines[j].strip().split(' ')[0].strip() in ["intervals"]):
					inIntervals = True
					continue
				if(inIntervals):
					key = lines[j].strip().split('=')[0].strip()
					val = lines[j].strip().split('=')[1].strip()
					if(key == "xmin"):
						#convert seconds to 100ns for boundaries
						curTime = val.strip('"')
						forward = str(float(val.strip('"')) + 0.01)
						backward = str(float(val.strip('"')) - 0.01)
					elif(key == "text"):
						#get the boundaries' labels and types
						curLabel = val.strip('"')
						prevType = curType
						if(curLabel in consonants):
							curType = "consonants"
						if(curLabel in vowels):
							curType = "vowels"
						if(curLabel in fric):
							curType = "fric";
						if(curLabel in nasals):
							curType = "nasals"
						if(curLabel in trill):
							curType = "trill"
						if(curLabel in stops):
							curType = "stops"
						if(curLabel in pause):
							curType = "pause"

						if(curType in ["stopes", "fric"] and not prevType in ["pause"]):
							toReplace.append((curTime, forward))
						if(curType in ["vowels"] and prevType in ["consonants", "fric", "stops", "nasals", "trill"]):
							toReplace.append((curTime, forward))
	for i in range(0, len(toReplace)):
		subs += 1
		print("subbing " + toReplace[i][0] + " with " + toReplace[i][1])
		res = re.sub(toReplace[i][0], toReplace[i][1], res)
		
	newFileHandle = open(file.split(".")[0] + "-subbed.TextGrid" , 'w');
	newFileHandle.write(res)
	
	newFileHandle.close()
	fileHandle.close()
print("subs: " + str(subs))