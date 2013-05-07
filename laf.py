#!/usr/bin/python
# -*- coding: utf-8 -*-

# list acronyms in file (*.tex)
import sys
import os
import subprocess
import re

camel_case = re.compile('(?:[A-Z])(?:[a-z])+(?:[A-Z])+') #e.g., WebRTC, QoS, QoE
only_word=re.compile("[^\w']")	# ignore alphaneumeric
parantheses = re.compile("\((.*)\)") # (words)

def print_list(_list):
	for t in _list:
		print t

def main(args):
    # find tex files in the current directory and the sub directory
    # using regex on find unix command
	findCommand = 'find . -type f -iregex \'.*\.tex\' -print'
    # print "Command:", findCommand
	texFiles = subprocess.check_output(findCommand, shell=True).split()
	# print texFiles
	# texFiles = filter(None, texFiles)
	
	# read words from abbr.ignore, these words will not be reported
	ignoreList = []
	k = file('accr.ignore').read()
	for word in k.split():
		ignoreList.append(word)
	ignoreList.sort()
	
	# create list
	inList = []
	newList = []
	for t in texFiles:
		print "Reading File:", t
		f = file(t).read()
		for word in f.split():
			# In latex some words are immediately followed by ~
			# Typically for \cite{} or \ref{}
			if (word.find('~')!=-1):
				w = word.split('~')
				# just keeping the first part of the word, 
				# everything after ~ is prolly a latex command
				word=w[0]
				# print w
			
			# Fetching words inside (parantheses)
			res = parantheses.search( word )
			if(res!=None):
				word=res.group(1)
				# print "parantheses", word
			
			# check if Word is uppercase
			# check CamelCASE or CamelCase
			if (word.isupper() or camel_case.match(word)!=None):
				accr=only_word.sub('', word)
				#acronyms are typically longer than a single letter.
				if(len(accr)>1): 
					# create list of acronyms already in list
					# create list of acronyms in 
					if(t.find('lists')!=-1): #t=="_0lists.tex" 
						if accr not in inList:
						    inList.append(accr)
					else:
						if accr not in newList:
						    newList.append(accr)
	newList.sort()
	# print "newList: ", newList
	inList.sort()
	# print "inList: ", inList
	print "Consider adding these"
	print_list(set(newList)-set(inList)-set(ignoreList))
	print "\nConsider removing these: (not in use):"
	print_list(set(inList)-set(newList)-set(ignoreList))

if __name__ == "__main__":
	main(sys.argv[1:])