#!/usr/bin/python
# -*- coding: UTF8 -*-

import sys
import codecs
import re
import glob, os

phones = ["AH", "r", "g", "y", "u0", "i1",
"b", "z", "f", "v", "i0", "uu1",
"t", "s", "q", "p", "AA", "ii1",
"SH", "k", "G", "UU0", "U1",
"j", "S", "l",  "d", "J", "II0", "I1",
"H", "D", "m", "aa", "A", "UU1",
"x", "T", "n", "uu0", "U0", "II1",
"d", "Z", "h", "ii0", "I0", "sil", 
"TH", "E", "w", "a", "u1", "sp"]


orgDir = sys.argv[1] #Directory if original segmentations (either manually or automatically)
corDir = sys.argv[2] #Directory of manually corrected segmentations

org = {}
cor = {}

for file in glob.glob(os.path.join(orgDir, '*.TextGrid')):
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

for file in glob.glob(os.path.join(corDir, '*.TextGrid')):
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
	
print org["ARA NORM  0052.TextGrid"]