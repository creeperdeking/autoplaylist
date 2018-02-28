import os
import pdb
import random
import sys
import time

""" Take a list of the m3u file lines and extract it in another list of this form: """
#		[[name,path,serialNumber], ...]
#	In wich -name stands for the song's name
#	        -path stands for the song's absolute path
#	        -serialNumber is ???
def extractM3U(fileContent):
	extracted = []
	previousLine = str()

	for e in fileContent:
		line = e.strip()
		if line[0] != '#': # skip comments
			spare = previousLine.split(':')[1].split(',')
			serialNumber = spare[0]
			name = spare[1]
			extracted.append([name,line,serialNumber])

		previousLine = line
	return extracted

""" Return a list containing the frequencies of apparition of each song"""
# The list is of this shape: [[song_abs_path, [0,1,0,2,0,0,0,0,1,...]],...]
# The frequencies represent the number of time a song follow this one
def getFreqencesDict(playlist):
	fqList = []
	for e in playlist:
		if not e in fqList:
			fqList.append(e)
	for i in range(len(fqList)):
		fqList[i] = [fqList[i],[0 for j in range(len(fqList))]]

	# Fill the fqList with fhe frequencies as described above
	for element in (fqList):
		song = element[0]
		for cptr, e in enumerate(playlist):
			if e == song:
				if cptr+1 < len(playlist):
					#Trouver la première apparition de la chanson
					for i, l in enumerate(fqList):
						if l[0] == playlist[cptr+1]:
							element[1][i] += 1
					# ajouter 1 a son numero
	return fqList

""" Save a playlist template into fileName (absolute path) """
# playlistExtracted sould look like this:
def savePlaylist(fileName, playlistExtracted):
	outFile = open(fileName, 'w')

	playlist = []
	for e in playlistExtracted:
		playlist.append(e[1])

	fqList = getFreqencesDict(playlist)

	outFile.write("#"+fileName.split('/')[-1].split('.')[-2])
	for name in fqList:
		outFile.write("\n")
		e = []
		for l in playlistExtracted:
			if l[1] == name[0]:
				e = l
				break

		outFile.write(e[0]+';'+e[1]+';'+e[2]+"\n")
		for i in range(len(fqList)): # fqList a la même longueur que la table de fréquences
			#import pdb
			#pdb.set_trace()
			elem = []
			for l in fqList:
				if l[0] == e[1]:
					elem = l[1]
			if i == len(fqList)-1:
				outFile.write(str(elem[i]))
			else:
				outFile.write(str(elem[i]) + ";")

""" Use VLC to play the given playlist """
def play(path):
	os.system("vlc \""+os.path.abspath(path)+"\" --quiet &")
	time.sleep(1)

""" Save the fiven playlist into m3u format """
def saveToM3U(name, finalPlaylist):
	outFile = open(os.path.abspath("./generatedPlaylists/"+name+".m3u"), 'w')

	outFile.write("#EXTM3U\n")
	for e in finalPlaylist:
		outFile.write("#EXTINF:"+e[2]+","+e[0]+"\n")
		outFile.write(e[1]+"\n")
	outFile.close()

""" Crée une nouvelle playlist avec un aléatoire guidé par les préférences de l'utilisateur """
def statisticalRandom(generatorTable, nbrSongs):
	finalPlaylist = []
	size = len(generatorTable[0][3])

	currentElement = generatorTable[random.randint(0, len(generatorTable)-1)]
	finalPlaylist.append(currentElement)
	# Now we generate a new random playlist:
	for e in range(nbrSongs):
		length = 0
		for occurences in currentElement[3]:
			length += occurences
		rand = 0
		if length != 0:
			rand = random.randrange(1, length+1)

			compare = 0
			for cptr, occurences in enumerate(currentElement[3]):
				compare += occurences
				if compare >= rand:
					currentElement = generatorTable[cptr]
					finalPlaylist.append(currentElement)
					break
		else:
			finalPlaylist.append(generatorTable[random.randrange(0, size-1)])

	return finalPlaylist

"""Generate a new playlist randomly """
def randomRandom(generatorTable, nbrSongs):
	finalPlaylist = []
	size = len(generatorTable[0][3])
	for e in range(nbrSongs):
		finalPlaylist.append(generatorTable[random.randrange(0, size-1)])

	return finalPlaylist

""" Generate and save a new playlist from filePath template """
def generatePlaylist(filePath, nbrSongs, statistical = True):
	inFile = open(os.path.abspath(filePath), 'r')
	content = inFile.readlines()

	generatorTable = []

	header = 1
	for e in content:
		if e[0] == '#':
			continue

		ligne = e.strip().split(";")
		if (header % 2):
			songName = ligne[0]
			path = ligne[1]
			tag = ligne[2]
			generatorTable.append([songName, path, tag])
		else:
			fqList = []
			for l in ligne:
				fqList.append(int(l))
			generatorTable[-1].append(fqList)

		header += 1

	# Generate the playlist using one of the two methods
	finalPlaylist = []
	if statistical:
		finalPlaylist = statisticalRandom(generatorTable, nbrSongs)
	else:
		finalPlaylist = randomRandom(generatorTable, nbrSongs)

	return finalPlaylist
